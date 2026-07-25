from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PKG_PARENT = str(Path(__file__).resolve().parents[1])


def spawn_worker(payload: bytes, engine: str | None, verbose: bool) -> None:
    """Fire off a detached worker that synthesizes and plays, then return.

    The Stop hook must not block on synthesis, so the reply plays after the
    session is already free.
    """
    command = [sys.executable, "-m", "tts", "speak", "--worker"]
    if engine:
        command += ["-e", engine]
    if verbose:
        command += ["-v"]

    env = {**os.environ, "PYTHONPATH": os.pathsep.join(
        [PKG_PARENT, os.environ.get("PYTHONPATH", "")]).rstrip(os.pathsep)}

    kwargs: dict = dict(stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, cwd=PKG_PARENT, env=env)
    if sys.platform.startswith("win"):
        kwargs["creationflags"] = (subprocess.DETACHED_PROCESS
                                   | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        kwargs["start_new_session"] = True

    child = subprocess.Popen(command, **kwargs)
    child.stdin.write(payload)
    child.stdin.close()
