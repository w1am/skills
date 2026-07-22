#!/bin/sh
case "$(uname)" in
    Darwin) afplay /System/Library/Sounds/Glass.aiff ;;
    *)      paplay --volume=30000 --property=media.role=event /usr/share/sounds/freedesktop/stereo/complete.oga ;;
esac
