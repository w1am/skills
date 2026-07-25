#!/usr/bin/env bash
#
# sudo askpass helper for Claude Code.
#
# Contract (imposed by `sudo -A`):
#   - sudo runs this program when it needs a password.
#   - Print the password to STDOUT and exit 0.
#   - Exit non-zero (and print nothing) to ABORT the sudo attempt
#     e.g. when the user cancels the dialog.
#   - sudo passes its prompt string as $1.
#
set -euo pipefail

PROMPT="${1:-Claude Code is requesting sudo access. Enter your password:}"

if password=$(zenity --entry --hide-text \
    --title="Claude Code · sudo" \
    --text="$PROMPT" \
    --timeout=60 \
    2>/dev/null); then
    printf '%s\n' "$password"
else
    exit 1
fi
