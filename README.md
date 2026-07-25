# Agents

A marketplace is a repo that Claude Code installs plugins from, the way a package
registry works for a language. This is a personal one. Each plugin is a bundle of
hooks and commands that changes how a session behaves at the terminal, and each is
installed on its own.

## Plugins

| Plugin                                 | What it does                                                     |
| -------------------------------------- | ---------------------------------------------------------------- |
| [`friday`](plugins/friday)             | Speaks each reply aloud, so you don't have to watch the terminal. |
| [`notify`](plugins/notify)             | Chimes when a turn ends.                                          |
| [`sudo-askpass`](plugins/sudo-askpass) | Lets the Bash tool run `sudo` via a GUI password dialog.          |
| [`tmux-title`](plugins/tmux-title)     | Names the tmux window after the project directory.                |
| [`workbench`](plugins/workbench)       | Recurring tasks as slash commands: naming review, logic deepening, release notes, plain-language explanations, session id. |

## Install

Merge into `~/.claude/settings.json` and restart. This registers the marketplace
and installs all five.

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

Everything works the moment it is installed except `friday`, which needs one
setup step: see [plugins/friday](plugins/friday/README.md).

## Manage

```sh
claude plugin list
claude plugin update <name>@w1am
claude plugin uninstall <name>@w1am
```

Try one without installing: `claude --plugin-dir plugins/friday`.
