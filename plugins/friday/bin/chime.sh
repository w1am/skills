#!/bin/sh
[ "${CC_TTS_CHIME:-1}" = "0" ] && exit 0
case "$(uname)" in
    Darwin) afplay /System/Library/Sounds/Glass.aiff ;;
    *)      paplay --volume=30000 --property=media.role=event /usr/share/sounds/freedesktop/stereo/complete.oga ;;
esac
