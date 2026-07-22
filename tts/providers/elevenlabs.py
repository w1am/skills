from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from .. import config
from ..registry import register
from .base import Provider, SynthesisFailed, Unavailable, Voice

API = "https://api.elevenlabs.io"
ALICE = "Xb7hH8MSUJpSbSDYk0k2"


@register
class ElevenLabs(Provider):
    name = "elevenlabs"
    metered = True

    def __init__(self) -> None:
        self.keyfile = Path(config.env("CC_TTS_EL_KEYFILE", str(config.ROOT / ".elevenlabs-key")))
        self.voice = config.env("CC_TTS_EL_VOICE", ALICE)
        self.model = config.env("CC_TTS_EL_MODEL", "eleven_turbo_v2_5")
        self.stability = config.env_float("CC_TTS_EL_STABILITY", 0.85)
        self.similarity = config.env_float("CC_TTS_EL_SIMILARITY", 0.90)
        self.speed = config.env_float("CC_TTS_EL_SPEED", 1.08)
        self.timeout = config.env_int("CC_TTS_EL_TIMEOUT", 20)

    def key(self) -> str:
        if inline := os.environ.get("ELEVENLABS_API_KEY", "").strip():
            return inline
        try:
            return self.keyfile.read_text().strip()
        except OSError:
            return ""

    def check(self) -> None:
        if not self.key():
            raise Unavailable(f"no api key in ELEVENLABS_API_KEY or {self.keyfile}")

    def request(self, path: str, payload: dict | None = None) -> bytes:
        url = f"{API}{path}"
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {"xi-api-key": self.key()}
        if data:
            headers["content-type"] = "application/json"
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, data=data, headers=headers), timeout=self.timeout
            ) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            raise SynthesisFailed(f"http {error.code}: {self.detail(error.read())}") from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise SynthesisFailed(f"network: {error}") from error

    @staticmethod
    def detail(body: bytes) -> str:
        try:
            payload = json.loads(body)
        except ValueError:
            return body[:160].decode(errors="replace")
        detail = payload.get("detail", payload)
        return detail.get("message", str(detail)) if isinstance(detail, dict) else str(detail)

    def synthesize(self, text: str, dest: Path) -> None:
        audio = self.request(
            f"/v1/text-to-speech/{self.voice}?output_format=mp3_44100_128",
            {
                "text": text,
                "model_id": self.model,
                "voice_settings": {
                    "stability": self.stability,
                    "similarity_boost": self.similarity,
                    "speed": self.speed,
                    "use_speaker_boost": True,
                },
            },
        )
        if not audio:
            raise SynthesisFailed("empty response body")
        dest.write_bytes(audio)

    def voices(self) -> list[Voice]:
        payload = json.loads(self.request("/v2/voices?page_size=100"))
        found = []
        for item in payload.get("voices", []):
            labels = item.get("labels") or {}
            library = item.get("category") == "professional"
            found.append(
                Voice(
                    id=item["voice_id"],
                    name=item["name"],
                    accent=labels.get("accent", ""),
                    gender=labels.get("gender", ""),
                    note="library voice, needs paid plan" if library else "",
                    usable=not library,
                )
            )
        return found

    def quota(self) -> str:
        try:
            payload = json.loads(self.request("/v1/user/subscription"))
        except SynthesisFailed as error:
            return f"unknown ({error})"
        used, limit = payload["character_count"], payload["character_limit"]
        return f"{used}/{limit} credits, {limit - used} left"

    def settings(self) -> dict[str, str]:
        return {
            "voice": self.voice,
            "model": self.model,
            "stability": str(self.stability),
            "speed": str(self.speed),
            "quota": self.quota() if self.key() else "no key",
        }
