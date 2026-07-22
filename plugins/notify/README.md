# notify

Plays a short completion chime when Claude Code finishes a turn, via a Stop hook.
Active as soon as it's installed.

## Install (agent, shell)

```sh
claude plugin marketplace add w1am/skills
claude plugin install notify@w1am --scope user
```

## Prerequisite

An event sound player: `afplay` (macOS, built in) or `paplay` (Linux, from
PulseAudio). On Linux also needs the freedesktop sound theme
(`/usr/share/sounds/freedesktop/…`, usually preinstalled).

## Verify (agent, shell)

```sh
bash "$(find ~/.claude/plugins/marketplaces/w1am -path '*/notify/bin/notify.sh' | head -1)"
```

You should hear one chime.

## How it works

`hooks/hooks.json` registers a Stop hook → `bin/notify.sh`, which plays a system
sound: `afplay` on macOS, `paplay` (freedesktop "complete" sound) elsewhere. If
you also run `tts`, both fire on Stop — the chime plays alongside the spoken reply.
