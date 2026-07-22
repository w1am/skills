from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .. import config
from ..registry import register
from .base import Provider, SynthesisFailed, Unavailable, Voice

ROW = re.compile(r"^(\S+)\s+(Male|Female)\s+(.*?)\s{2,}(.*)$")


@register
class Edge(Provider):
    name = "edge"

    def __init__(self) -> None:
        self.voice = config.env("CC_TTS_VOICE", "en-IE-EmilyNeural")
        self.rate = config.env("CC_TTS_RATE", "+6%")
        self.pitch = config.env("CC_TTS_PITCH", "-5Hz")
        self.timeout = config.env_int("CC_TTS_EDGE_TIMEOUT", 30)

    def binary(self) -> str | None:
        return shutil.which("edge-tts")

    def check(self) -> None:
        if not self.binary():
            raise Unavailable("edge-tts not on PATH")

    def run(self, args: list[str]) -> str:
        binary = self.binary()
        if not binary:
            raise SynthesisFailed("edge-tts not on PATH")
        result = subprocess.run(
            [binary, *args], capture_output=True, text=True, timeout=self.timeout
        )
        if result.returncode != 0:
            raise SynthesisFailed(result.stderr.strip()[:160] or "edge-tts failed")
        return result.stdout

    def synthesize(self, text: str, dest: Path) -> None:
        self.run(["--voice", self.voice, f"--rate={self.rate}", f"--pitch={self.pitch}",
                  "--text", text, "--write-media", str(dest)])
        if not dest.exists() or dest.stat().st_size == 0:
            raise SynthesisFailed("wrote empty file")

    def voices(self) -> list[Voice]:
        found = []
        for line in self.run(["--list-voices"]).splitlines():
            if match := ROW.match(line.rstrip()):
                voice, gender, _, description = match.groups()
                found.append(
                    Voice(id=voice, name=voice, accent=voice.rsplit("-", 1)[0],
                          gender=gender.lower(), note=description.strip())
                )
        return found

    def settings(self) -> dict[str, str]:
        return {"voice": self.voice, "rate": self.rate, "pitch": self.pitch}
