#!/usr/bin/env bash
# Stop-hook entry. Portable across Linux, macOS, and Windows (Git Bash).
# Media check, single-speaker lock, and detached playback all live in Python;
# this only reads the reply on stdin and hands it to the launcher, which returns
# fast after spawning a detached worker.
set -uo pipefail

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
exec bash "$SELF/claude-tts" speak
