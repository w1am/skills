from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


class Unavailable(Exception):
    """Provider cannot serve any request. Skip it and move down the chain."""


class SynthesisFailed(Exception):
    """Provider was usable but this request failed."""


@dataclass(frozen=True)
class Voice:
    id: str
    name: str
    accent: str = ""
    gender: str = ""
    note: str = ""
    usable: bool = True


class Provider(ABC):
    name: str = ""
    suffix: str = ".mp3"
    metered: bool = False

    @abstractmethod
    def check(self) -> None:
        """Raise Unavailable if this provider cannot serve requests."""

    @abstractmethod
    def synthesize(self, text: str, dest: Path) -> None:
        """Write audio for text to dest. Raise SynthesisFailed on error."""

    def voices(self) -> list[Voice]:
        return []

    def settings(self) -> dict[str, str]:
        return {}
