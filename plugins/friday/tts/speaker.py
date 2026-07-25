from __future__ import annotations

import tempfile
from contextlib import contextmanager
from pathlib import Path

from . import audio, config, registry
from .providers.base import Provider, SynthesisFailed, Unavailable


class NothingSpoke(RuntimeError):
    def __init__(self, failures: list[str]) -> None:
        super().__init__("no provider could speak:\n  " + "\n  ".join(failures))
        self.failures = failures


@contextmanager
def scratch(suffix: str):
    handle = tempfile.NamedTemporaryFile(prefix="cc-tts-", suffix=suffix, delete=False)
    handle.close()
    path = Path(handle.name)
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


def resolve(name: str) -> Provider:
    provider = registry.create(name)
    provider.check()
    return provider


def speak(text: str, names: tuple[str, ...] | None = None) -> str:
    failures: list[str] = []
    for name in names or config.chain():
        try:
            provider = resolve(name)
        except (KeyError, Unavailable) as error:
            config.log.debug("%s: %s", name, error)
            failures.append(f"{name}: {error}")
            continue
        with scratch(provider.suffix) as path:
            try:
                provider.synthesize(text, path)
            except SynthesisFailed as error:
                config.log.debug("%s: %s", name, error)
                failures.append(f"{name}: {error}")
                continue
            config.log.debug("%s: ok", name)
            audio.play(path)
            return name
    raise NothingSpoke(failures)
