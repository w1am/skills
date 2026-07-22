# tmux-title

Names the current tmux window after the project directory while Claude Code is
running, then restores tmux's automatic renaming when the session ends. No-op
outside tmux. Active as soon as it's installed; no setup or dependencies beyond
`tmux`.

## Install (agent, shell)

```sh
claude plugin marketplace add w1am/skills
claude plugin install tmux-title@w1am --scope user
```

## Verify

Start a Claude Code session inside a tmux window; the window title becomes
`cc:<project-dir>`. It reverts to automatic renaming when the session ends. There
is nothing to run standalone — the hooks call `tmux` directly.

## How it works

`hooks/hooks.json`:

- **SessionStart** → `tmux rename-window "cc:<dir>"` when `$TMUX` is set.
- **SessionEnd** → `tmux set-option -w automatic-rename on`.
