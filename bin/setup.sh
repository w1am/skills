#!/usr/bin/env bash
set -eu

# Default engine is edge-tts (free, no key), installed as a global uv tool so the
# launcher finds it on PATH. --kokoro adds the offline engine: a pinned-Python venv
# (onnxruntime ships no wheels past 3.12) plus a ~338MB model download.

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT="$(dirname "$SELF")"
VENV="$ROOT/tts-venv"
MODELS="$ROOT/tts-models"
PYTHON_VERSION=3.12
KOKORO_PKGS="kokoro-onnx soundfile"
KOKORO_BASE="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"

PATH="$HOME/.local/bin:$PATH"
export PATH

want_kokoro=0
for arg in "$@"; do
  case "$arg" in
    --kokoro) want_kokoro=1 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }

if ! command -v uv >/dev/null 2>&1; then
  echo "==> installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  PATH="$HOME/.local/bin:$PATH"
  export PATH
fi
command -v uv >/dev/null || { echo "uv still not on PATH; open a new shell and rerun" >&2; exit 1; }

if ! command -v edge-tts >/dev/null 2>&1; then
  echo "==> installing edge-tts (default engine)"
  uv tool install --quiet edge-tts
fi

if [ "$want_kokoro" = 1 ]; then
  echo "==> building offline engine venv ($KOKORO_PKGS)"
  uv venv --quiet --allow-existing --python "$PYTHON_VERSION" "$VENV"
  uv pip install --quiet --python "$VENV/bin/python" $KOKORO_PKGS
  mkdir -p "$MODELS"
  for f in kokoro-v1.0.onnx voices-v1.0.bin; do
    if [ -s "$MODELS/$f" ]; then echo "    have $f"; continue; fi
    echo "    downloading $f"
    curl -fSL "$KOKORO_BASE/$f" -o "$MODELS/$f"
  done
fi

echo
echo "==> done. checking status:"
"$SELF/claude-tts" doctor
