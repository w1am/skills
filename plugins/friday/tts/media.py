from __future__ import annotations

import shutil
import subprocess
import sys

from . import config


def is_playing() -> bool:
    """Best-effort: is other audio playing right now? Never raises.

    Only Linux is reliably detectable via MPRIS. Elsewhere we assume silence
    rather than guess, so the reply always gets spoken.
    """
    if config.env("CC_TTS_IGNORE_MEDIA"):
        return False
    try:
        if sys.platform.startswith("linux"):
            return _linux_playing()
    except Exception as error:
        config.log.debug("media check failed: %s", error)
    return False


def _linux_playing() -> bool:
    if shutil.which("playerctl"):
        result = subprocess.run(["playerctl", "-a", "status"],
                                capture_output=True, text=True, timeout=2)
        return "Playing" in result.stdout
    if not shutil.which("busctl"):
        return False
    listing = subprocess.run(["busctl", "--user", "list"],
                             capture_output=True, text=True, timeout=2)
    for line in listing.stdout.splitlines():
        service = line.split(" ", 1)[0]
        if not service.startswith("org.mpris.MediaPlayer2."):
            continue
        status = subprocess.run(
            ["busctl", "--user", "get-property", service, "/org/mpris/MediaPlayer2",
             "org.mpris.MediaPlayer2.Player", "PlaybackStatus"],
            capture_output=True, text=True, timeout=2)
        if "Playing" in status.stdout:
            return True
    return False
