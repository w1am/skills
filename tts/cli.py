from __future__ import annotations

import argparse
import json
import sys

from . import audio, config, registry, speaker, text
from .providers.base import SynthesisFailed, Unavailable


def cmd_speak(args) -> int:
    payload = sys.stdin.read()
    try:
        message = json.loads(payload).get("last_assistant_message") or ""
    except ValueError:
        message = payload
    spoken = text.spoken(message, config.max_chars())
    if not spoken:
        return 0
    return say(spoken, args)


def cmd_say(args) -> int:
    return say(" ".join(args.words) or sys.stdin.read().strip(), args)


def say(spoken: str, args) -> int:
    names = (args.engine,) if args.engine else None
    try:
        used = speaker.speak(spoken, names)
    except speaker.NothingSpoke as error:
        print(error, file=sys.stderr)
        return 1
    if args.verbose:
        print(f"[{used}] {spoken}", file=sys.stderr)
    return 0


def cmd_voices(args) -> int:
    for name in [args.engine] if args.engine else registry.names():
        try:
            provider = speaker.resolve(name)
            found = provider.voices()
        except (KeyError, Unavailable, SynthesisFailed) as error:
            print(f"{name}: {error}", file=sys.stderr)
            continue
        print(f"\n{name} ({len(found)} voices)")
        for voice in found:
            if args.usable and not voice.usable:
                continue
            if args.grep and args.grep.lower() not in str(voice).lower():
                continue
            mark = " " if voice.usable else "x"
            print(f" {mark} {voice.id:<24} {voice.name[:28]:<28} "
                  f"{voice.accent:<10} {voice.gender:<7} {voice.note[:34]}")
    return 0


def cmd_audition(args) -> int:
    provider = speaker.resolve(args.engine)
    sample = config.sample_text()
    for voice in args.voices:
        setattr(provider, "voice", voice)
        print(f"\n[{args.engine}] {voice}")
        with speaker.scratch(provider.suffix) as path:
            try:
                provider.synthesize(sample, path)
            except SynthesisFailed as error:
                print(f"  failed: {error}", file=sys.stderr)
                continue
            audio.play(path)
    return 0


def cmd_doctor(args) -> int:
    active = config.chain()
    print(f"chain:  {' -> '.join(active)}")
    found = audio.player()
    print(f"player: {found[0] if found else 'NONE FOUND'}")
    ordered = sorted(registry.names(),
                     key=lambda name: (active.index(name) if name in active else len(active), name))
    for name in ordered:
        marker = f"{active.index(name) + 1}." if name in active else "  "
        try:
            provider = speaker.resolve(name)
        except (KeyError, Unavailable) as error:
            print(f"\n{marker} {name}: unavailable, {error}")
            continue
        meter = " (metered)" if provider.metered else ""
        print(f"\n{marker} {name}: ready{meter}")
        for key, value in provider.settings().items():
            print(f"      {key:<12} {value}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-e", "--engine",
                        help=f"pin one provider ({', '.join(registry.names())})")
    common.add_argument("-v", "--verbose", action="store_true", help="report which engine ran")

    parser = argparse.ArgumentParser(prog="tts", description="Speak Claude Code replies aloud.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("speak", parents=[common],
                   help="read hook JSON on stdin and speak its <speak> block")

    say_parser = sub.add_parser("say", parents=[common], help="speak arbitrary text")
    say_parser.add_argument("words", nargs="*")

    voices_parser = sub.add_parser("voices", parents=[common], help="list voices")
    voices_parser.add_argument("-u", "--usable", action="store_true", help="hide gated voices")
    voices_parser.add_argument("-g", "--grep", help="filter by substring")

    audition_parser = sub.add_parser("audition", parents=[common],
                                     help="play a sample in each voice")
    audition_parser.add_argument("voices", nargs="+")

    sub.add_parser("doctor", parents=[common],
                   help="show provider status and resolved settings")
    return parser


COMMANDS = {
    "speak": cmd_speak,
    "say": cmd_say,
    "voices": cmd_voices,
    "audition": cmd_audition,
    "doctor": cmd_doctor,
}


def main(argv: list[str] | None = None) -> int:
    config.configure_logging()
    args = build_parser().parse_args(argv)
    if args.command == "audition" and not args.engine:
        print("audition needs --engine", file=sys.stderr)
        return 2
    try:
        return COMMANDS[args.command](args)
    except KeyboardInterrupt:
        return 130
