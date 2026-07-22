# dev-commands

Personal slash commands.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install dev-commands@claude-plugins
```

## Commands

| Command | What it does |
|---------|--------------|
| `/session` | Copy the current session id to the clipboard (`wl-copy`/`xclip`/`xsel`/`pbcopy`). |
| `/cut-release <new> [prev] [--style customers\|developers\|internal]` | Write release notes for a version range and update the GitHub draft release. |
| `/deepen [target]` | Simplify code by simplifying the business logic and model, not by extracting helpers. Fans out subagents to find hidden concepts, then proposes a simpler model before editing. |
