# w1am/agents

Personal Claude Code marketplace.

## Install

Merge into `~/.claude/settings.json` and restart. This registers the marketplace and
installs all five.

```json
{
  "extraKnownMarketplaces": {
    "w1am": { "source": { "source": "github", "repo": "w1am/agents" } }
  },
  "enabledPlugins": {
    "friday@w1am": true,
    "notify@w1am": true,
    "sudo-askpass@w1am": true,
    "tmux-title@w1am": true,
    "workbench@w1am": true
  }
}
```

Or one at a time: `claude plugin marketplace add w1am/agents`, then
`claude plugin install <name>@w1am`.

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
