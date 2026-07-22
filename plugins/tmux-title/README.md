# tmux-title

Names the current tmux window after the project directory while Claude Code is
running, then restores tmux's automatic renaming when the session ends. No-op
outside tmux.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install tmux-title@w1am
```

## How it works

- **SessionStart** → `tmux rename-window "cc:<dir>"` when `$TMUX` is set.
- **SessionEnd** → `tmux set-option -w automatic-rename on`.
