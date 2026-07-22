# tts

Speak Claude Code's replies aloud. Ships a **Stop hook** that reads each reply, a
fallback **chain of TTS engines** — `edge` (free, no key), `kokoro` (offline),
`elevenlabs` (best quality, metered) — and a **Spoken** output style that makes
replies sound right for the ear.

The hook extracts the `<speak>…</speak>` block the Spoken style emits. Without
that style it falls back to speaking the first paragraph.

## Install (agent, shell)

```sh
claude plugin marketplace add w1am/skills
claude plugin install tts@w1am --scope user
```

## Setup (required, one step)

The engine isn't bundled; a setup script installs it. Locate and run it:

```sh
tts_bin="$(dirname "$(find ~/.claude/plugins/marketplaces/w1am -path '*/tts/bin/setup.sh' | head -1)")"
bash "$tts_bin/setup.sh"            # default: edge-tts as a global uv tool
bash "$tts_bin/setup.sh" --kokoro  # optional: offline engine + ~350MB model
```

`setup.sh` installs [uv](https://docs.astral.sh/uv/) if missing, then `edge-tts`.
It needs `python3` and an audio player on `PATH`.

### Audio player (one system dependency)

Playback uses the first found of: `mpv`, `afplay` (macOS), `ffplay` (ffmpeg),
`paplay`, `aplay`. Install one, e.g. `sudo apt install mpv` or `brew install mpv`.

## Verify (agent, shell)

```sh
"$tts_bin/claude-tts" doctor          # engine chain, player, per-engine status
"$tts_bin/claude-tts" say "hello"     # speak a test phrase
```

Then select the voice output style for speech-tuned replies. In a Claude Code
session: `/output-style Spoken`, or set `"outputStyle": "Spoken"` in settings.

## Engines

| Engine | Setup | Notes |
|--------|-------|-------|
| `edge` | `setup.sh` (uv tool, default) | Free, no key, needs network. Default voice. |
| `kokoro` | `setup.sh --kokoro` | Offline, ~350MB model, better voice. |
| `elevenlabs` | key in `~/.claude/.elevenlabs-key` or `ELEVENLABS_API_KEY` | Best quality, metered. |

Default chain is `edge, kokoro, elevenlabs` — the first ready one wins. Reorder
with `CC_TTS_CHAIN`, or pin one with `CC_TTS_ENGINE`.

## Configuration (env vars)

Set these in the Claude Code environment (e.g. `env` in settings.json) to change
behavior:

| Var | Default | Effect |
|-----|---------|--------|
| `CC_TTS_ENGINE` | — | Pin a single engine, ignore the chain. |
| `CC_TTS_CHAIN` | `edge,kokoro,elevenlabs` | Comma-separated fallback order. |
| `CC_TTS_MAX_CHARS` | `2000` | Truncate longer replies. |
| `CC_TTS_IGNORE_MEDIA` | — | Speak even while other media is playing. |
| `CC_TTS_VOICE` / `CC_TTS_RATE` / `CC_TTS_PITCH` | | Edge voice knobs. |
| `CC_TTS_KOKORO_VOICE` / `CC_TTS_KOKORO_SPEED` | | Kokoro voice knobs. |
| `CC_TTS_EL_VOICE` / `CC_TTS_EL_MODEL` | | ElevenLabs voice knobs. |
| `CC_TTS_DEBUG=1` | — | Log to `~/.claude/tts.log`. |

List available voices per engine:

```sh
"$tts_bin/claude-tts" voices -e edge -u
"$tts_bin/claude-tts" audition -e edge en-IE-EmilyNeural en-GB-SoniaNeural
```

## How it works

`hooks/hooks.json` registers a Stop hook → `bin/speak.sh`. That script skips if
other audio is playing, takes a single-speaker lock, and pipes the reply into
`bin/claude-tts speak`. The Python package (`tts/`) extracts and cleans the
spoken text, walks the engine chain until one synthesizes audio, and plays it.
