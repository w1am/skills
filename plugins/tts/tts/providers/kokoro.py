from __future__ import annotations

from functools import cache
from pathlib import Path

from .. import config
from ..registry import register
from .base import Provider, SynthesisFailed, Unavailable, Voice

BRITISH_FEMALE = "bf_"


@cache
def engine(models: Path):
    from kokoro_onnx import Kokoro

    return Kokoro(str(models / "kokoro-v1.0.onnx"), str(models / "voices-v1.0.bin"))


@register
class Kokoro(Provider):
    name = "kokoro"
    suffix = ".wav"

    def __init__(self) -> None:
        self.models = Path(config.env("CC_TTS_KOKORO_MODELS", str(config.ROOT / "tts-models")))
        self.voice = config.env("CC_TTS_KOKORO_VOICE", "bf_emma")
        self.speed = config.env_float("CC_TTS_KOKORO_SPEED", 1.06)
        self.lang = config.env("CC_TTS_KOKORO_LANG", "en-gb")

    def check(self) -> None:
        for filename in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
            if not (self.models / filename).is_file():
                raise Unavailable(f"missing model file {self.models / filename}")
        try:
            import kokoro_onnx  # noqa: F401
        except ImportError as error:
            raise Unavailable(f"kokoro_onnx not importable: {error}") from error

    def synthesize(self, text: str, dest: Path) -> None:
        import soundfile

        try:
            samples, rate = engine(self.models).create(
                text, voice=self.voice, speed=self.speed, lang=self.lang
            )
        except Exception as error:
            raise SynthesisFailed(str(error)) from error
        soundfile.write(str(dest), samples, rate)

    def voices(self) -> list[Voice]:
        accents = {"a": "american", "b": "british", "e": "spanish", "f": "french",
                   "h": "hindi", "i": "italian", "j": "japanese", "p": "portuguese", "z": "chinese"}
        genders = {"m": "male", "f": "female"}
        found = []
        for name in sorted(engine(self.models).get_voices()):
            prefix = name.split("_")[0]
            found.append(
                Voice(
                    id=name,
                    name=name.split("_", 1)[-1].title(),
                    accent=accents.get(prefix[:1], ""),
                    gender=genders.get(prefix[1:2], ""),
                )
            )
        return found

    def settings(self) -> dict[str, str]:
        return {"voice": self.voice, "speed": str(self.speed),
                "lang": self.lang, "models": str(self.models)}
