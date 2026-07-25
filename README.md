# w1am/skills

Personal Claude Code marketplace.

## Install

```sh
claude plugin marketplace add w1am/skills
for p in friday notify sudo-askpass tmux-title workbench; do claude plugin install "$p@w1am"; done
```

Everything is active on install except `friday`, which needs one setup step: see
[plugins/friday](plugins/friday/README.md).

## Plugins

| Plugin                                 | What it does                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [`friday`](plugins/friday)             | Speaks each reply aloud (`edge`, `kokoro`, `elevenlabs`) and ships the Spoken output style.       |
| [`notify`](plugins/notify)             | Chime when a turn ends.                                                                           |
| [`sudo-askpass`](plugins/sudo-askpass) | Routes `sudo` prompts through a GUI askpass helper.                                               |
| [`tmux-title`](plugins/tmux-title)     | Renames the tmux window to the project dir.                                                       |
| [`workbench`](plugins/workbench)       | Skills as commands: `/naming-review`, `/deepen`, `/cut-release`, `/business-context`, `/session`. |

## Manage

```sh
claude plugin list
claude plugin update <name>@w1am
claude plugin uninstall <name>@w1am
```

Try one without installing: `claude --plugin-dir plugins/friday`.
