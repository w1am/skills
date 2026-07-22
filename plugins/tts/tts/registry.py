from __future__ import annotations

import importlib
import pkgutil

from .providers.base import Provider

_REGISTRY: dict[str, type[Provider]] = {}
_LOADED = False


def register(cls: type[Provider]) -> type[Provider]:
    if not cls.name:
        raise ValueError(f"{cls.__qualname__} must define a name")
    _REGISTRY[cls.name] = cls
    return cls


def _discover() -> None:
    global _LOADED
    if _LOADED:
        return
    from . import providers

    for module in pkgutil.iter_modules(providers.__path__):
        if module.name not in ("base",) and not module.name.startswith("_"):
            importlib.import_module(f"{providers.__name__}.{module.name}")
    _LOADED = True


def names() -> list[str]:
    _discover()
    return sorted(_REGISTRY)


def create(name: str) -> Provider:
    _discover()
    if name not in _REGISTRY:
        raise KeyError(f"unknown provider {name!r}, have: {', '.join(sorted(_REGISTRY))}")
    return _REGISTRY[name]()
