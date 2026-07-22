# notify

Plays a short completion chime when Claude Code finishes a turn, via a Stop hook.

## Install

```
/plugin marketplace add w1am/skills
/plugin install notify@w1am
```

## How it works

`hooks/hooks.json` registers a Stop hook → `bin/notify.sh`, which plays a system
sound: `afplay` on macOS, `paplay` (freedesktop "complete" sound) elsewhere.

If you also run the `tts` plugin, both fire on Stop — the chime plays alongside
the spoken reply.
