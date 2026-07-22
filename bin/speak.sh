#!/usr/bin/env bash
set -uo pipefail

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
TTS="$SELF/claude-tts"
LOCKFILE="/tmp/cc-tts-$(id -u).lock"

media_playing() {
  local svc status
  for svc in $(busctl --user list 2>/dev/null | awk '/^org\.mpris\.MediaPlayer2\./{print $1}'); do
    status=$(busctl --user get-property "$svc" /org/mpris/MediaPlayer2 \
      org.mpris.MediaPlayer2.Player PlaybackStatus 2>/dev/null)
    case "$status" in
      *Playing*) return 0 ;;
    esac
  done
  return 1
}

[ -x "$TTS" ] || exit 0
if [ -z "${CC_TTS_IGNORE_MEDIA:-}" ] && media_playing; then
  exit 0
fi

payload=$(cat)
[ -n "${payload// /}" ] || exit 0

setsid bash -c '
  exec 9>"$3"
  flock -n 9 || exit 0
  printf "%s" "$2" | exec "$1" speak
' _ "$TTS" "$payload" "$LOCKFILE" >/dev/null 2>&1 < /dev/null &

exit 0
