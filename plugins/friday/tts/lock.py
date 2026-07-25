from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


def lockfile() -> Path:
    name = f"cc-tts-{os.getuid()}.lock" if hasattr(os, "getuid") else "cc-tts.lock"
    return Path(tempfile.gettempdir()) / name


@contextmanager
def single_instance():
    """Yield True if this process took the lock, False if another holds it.

    Non-blocking: a second speaker sees False and should bow out.
    """
    path = lockfile()
    handle = open(path, "a+")
    try:
        if _acquire(handle):
            yield True
        else:
            yield False
    finally:
        handle.close()


def _acquire(handle) -> bool:
    try:
        import fcntl
    except ImportError:
        return _acquire_windows(handle)
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _acquire_windows(handle) -> bool:
    import msvcrt

    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        return True
    except OSError:
        return False
