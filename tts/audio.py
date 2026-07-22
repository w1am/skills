from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from . import config

PLAYERS = (
    ("mpv", ["--really-quiet", "--no-video", "--no-terminal"]),
    ("afplay", []),
    ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]),
    ("paplay", []),
    ("aplay", ["-q"]),
)

STREAM_NAME = "Claude TTS"
STREAM_PROPS = f"application.name='{STREAM_NAME}' application.id={STREAM_NAME}"

LEVEL = "speechnorm=e=12.5:r=0.0005:l=1,alimiter=limit=0.95:level=disabled"

EXTRA = {
    "mpv": [f"--audio-client-name={STREAM_NAME}", f"--af=lavfi=[{LEVEL}]"],
}


def player() -> tuple[str, list[str]] | None:
    for command, flags in PLAYERS:
        if path := shutil.which(command):
            return path, flags
    return None


def play(path: Path) -> None:
    found = player()
    if not found:
        raise RuntimeError(f"no audio player found, tried: {', '.join(p for p, _ in PLAYERS)}")
    command, flags = found
    extra = EXTRA.get(Path(command).name, [])
    subprocess.run([command, *flags, *extra, str(path)], check=False,
                   env={**os.environ, "PULSE_PROP": STREAM_PROPS},
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
