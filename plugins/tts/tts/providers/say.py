from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from .. import config
from ..registry import register
from .base import Provider, SynthesisFailed, Unavailable, Voice

ROW = re.compile(r"^(.+?)\s{2,}([A-Za-z][\w-]+)\s*#\s*(.*)$")


@register
class Say(Provider):
    name = "say"
    suffix = ".aiff"

    def __init__(self) -> None:
        self.voice = config.env("CC_TTS_SAY_VOICE")
        self.rate = config.env("CC_TTS_SAY_RATE")
        self.timeout = config.env_int("CC_TTS_SAY_TIMEOUT", 30)

    def check(self) -> None:
        if sys.platform != "darwin":
            raise Unavailable("say is macOS-only")
        if not shutil.which("say"):
            raise Unavailable("say not on PATH")

    def args(self) -> list[str]:
        flags: list[str] = []
        if self.voice:
            flags += ["-v", self.voice]
        if self.rate:
            flags += ["-r", self.rate]
        return flags

    def synthesize(self, text: str, dest: Path) -> None:
        result = subprocess.run(
            ["say", *self.args(), "-o", str(dest), "-f", "-"],
            input=text.encode(), capture_output=True, timeout=self.timeout,
        )
        if result.returncode != 0:
            raise SynthesisFailed(result.stderr.decode(errors="replace").strip()[:160]
                                  or "say failed")
        if not dest.exists() or dest.stat().st_size == 0:
            raise SynthesisFailed("wrote empty file")

    def voices(self) -> list[Voice]:
        listing = subprocess.run(["say", "-v", "?"], capture_output=True,
                                 text=True, timeout=self.timeout)
        found = []
        for line in listing.stdout.splitlines():
            if match := ROW.match(line.rstrip()):
                name, lang, sample = match.groups()
                found.append(Voice(id=name.strip(), name=name.strip(),
                                   accent=lang, note=sample.strip()))
        return found

    def settings(self) -> dict[str, str]:
        return {"voice": self.voice or "(system default)",
                "rate": self.rate or "(system default)"}
