from __future__ import annotations

import base64
import os
import shutil
import subprocess
import sys
from pathlib import Path

STREAM_NAME = "Claude TTS"
STREAM_PROPS = f"application.name='{STREAM_NAME}' application.id={STREAM_NAME}"

LEVEL = "speechnorm=e=12.5:r=0.0005:l=1,alimiter=limit=0.95:level=disabled"

PATH_PLAYERS = (
    ("mpv", ["--really-quiet", "--no-video", "--no-terminal"]),
    ("afplay", []),
    ("ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]),
    ("paplay", []),
    ("pw-play", []),
    ("aplay", ["-q"]),
    ("cvlc", ["--play-and-exit", "--intf", "dummy", "--quiet"]),
)

EXTRA = {
    "mpv": [f"--audio-client-name={STREAM_NAME}", f"--af=lavfi=[{LEVEL}]"],
}

WINDOWS_PLAYBACK = r"""
$ErrorActionPreference = 'Stop'
$path = $env:CC_TTS_AUDIO
Add-Type -Name Win -Namespace Mci -MemberDefinition '[DllImport("winmm.dll", CharSet=CharSet.Auto)] public static extern int mciSendString(string command, System.Text.StringBuilder buffer, int bufferSize, System.IntPtr hwndCallback);'
[void][Mci.Win]::mciSendString("open `"$path`" type mpegvideo alias ccTts", $null, 0, [System.IntPtr]::Zero)
[void][Mci.Win]::mciSendString("play ccTts wait", $null, 0, [System.IntPtr]::Zero)
[void][Mci.Win]::mciSendString("close ccTts", $null, 0, [System.IntPtr]::Zero)
"""


def path_player() -> tuple[str, list[str]] | None:
    for command, flags in PATH_PLAYERS:
        if path := shutil.which(command):
            return path, flags
    return None


def powershell() -> str | None:
    if not sys.platform.startswith("win"):
        return None
    return shutil.which("powershell") or shutil.which("pwsh")


def player() -> str | None:
    if found := path_player():
        return found[0]
    if shell := powershell():
        return f"{Path(shell).name} (built-in)"
    return None


def play(path: Path) -> None:
    found = path_player()
    if found:
        command, flags = found
        extra = EXTRA.get(Path(command).stem, [])
        subprocess.run([command, *flags, *extra, str(path)], check=False,
                       env={**os.environ, "PULSE_PROP": STREAM_PROPS},
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    if shell := powershell():
        encoded = base64.b64encode(WINDOWS_PLAYBACK.encode("utf-16-le")).decode()
        subprocess.run([shell, "-NoProfile", "-NonInteractive",
                        "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded],
                       check=False, env={**os.environ, "CC_TTS_AUDIO": str(path)},
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    tried = ", ".join(p for p, _ in PATH_PLAYERS)
    raise RuntimeError(f"no audio player found, tried: {tried}")
