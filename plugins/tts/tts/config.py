from __future__ import annotations

import logging
import os
from pathlib import Path

ROOT = Path(os.environ.get("CC_TTS_ROOT", "").strip() or Path.home() / ".claude")
DEFAULT_CHAIN = ("edge", "kokoro", "elevenlabs")
SAMPLE = "Done. The timeout was in seconds, not milliseconds. Three of four tests now pass."

log = logging.getLogger("tts")


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, "").strip() or default


def env_float(key: str, default: float) -> float:
    try:
        return float(env(key))
    except ValueError:
        return default


def env_int(key: str, default: int) -> int:
    try:
        return int(env(key))
    except ValueError:
        return default


def chain() -> tuple[str, ...]:
    if pinned := env("CC_TTS_ENGINE"):
        return (pinned,)
    if custom := env("CC_TTS_CHAIN"):
        return tuple(part.strip() for part in custom.split(",") if part.strip())
    return DEFAULT_CHAIN


def max_chars() -> int:
    return env_int("CC_TTS_MAX_CHARS", 2000)


def sample_text() -> str:
    return env("CC_TTS_SAMPLE", SAMPLE)


def configure_logging() -> None:
    if not env("CC_TTS_DEBUG"):
        logging.disable(logging.CRITICAL)
        return
    path = Path(env("CC_TTS_LOG", str(ROOT / "tts.log")))
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
        handlers=[logging.FileHandler(path)],
    )
