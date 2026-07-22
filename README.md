# w1am/skills

A personal Claude Code marketplace (handle `w1am`), built to be installed and
operated by an autonomous agent from these docs alone. Every step is a shell
command, not a `/slash` action in the TUI — hand an agent the raw markdown and it
can register the marketplace, install any plugin, set it up, and verify it.

See [AGENTS.md](AGENTS.md) for the one-shot runbook. Each plugin's own README is a
self-contained runbook for that plugin.

## Install (agent, shell)

```sh
# Register the marketplace once per machine (idempotent). Accepts a GitHub
# owner/repo, a git URL, or a local path.
claude plugin marketplace add w1am/skills

# Install the plugins you want. --scope user installs for the whole user account.
claude plugin install tts@w1am          --scope user
claude plugin install notify@w1am       --scope user
claude plugin install sudo-askpass@w1am --scope user
claude plugin install tmux-title@w1am   --scope user
claude plugin install w1am-skills@w1am  --scope user

# Confirm what's installed.
claude plugin list
```

All plugins are active as soon as they're installed, **except `tts`**, which needs
one post-install setup step — see [plugins/tts](plugins/tts/README.md).

## Plugins

| Plugin | Type | Active on install | What it does |
|--------|------|-------------------|--------------|
| [`tts`](plugins/tts) | Stop hook + output style | after `bin/setup.sh` | Speaks each reply aloud through a fallback chain of TTS engines (`edge`, `kokoro`, `elevenlabs`); ships the **Spoken** output style. |
| [`notify`](plugins/notify) | Stop hook | yes | Plays a completion chime when a turn ends. |
| [`sudo-askpass`](plugins/sudo-askpass) | PreToolUse hook | yes | Lets the Bash tool run `sudo` via a GUI askpass helper. |
| [`tmux-title`](plugins/tmux-title) | Session hooks | yes | Renames the tmux window to the project dir while Claude runs. |
| [`w1am-skills`](plugins/w1am-skills) | Skills | yes | Skills runnable as `/commands`: `/naming-review`, `/deepen`, `/cut-release`, `/session`. |

## Manage (agent, shell)

```sh
claude plugin list                        # installed plugins
claude plugin details <name>@w1am         # component inventory + token cost
claude plugin marketplace update w1am     # pull latest marketplace metadata
claude plugin update <name>@w1am          # update one plugin (restart to apply)
claude plugin uninstall <name>@w1am       # remove one plugin
claude plugin marketplace remove w1am     # deregister the marketplace
claude plugin validate <path> --strict    # validate a plugin/marketplace manifest
```

To try a plugin without installing it, load it for a single session:
`claude --plugin-dir plugins/tts`.

## Layout

```
.claude-plugin/marketplace.json   # marketplace manifest, lists every plugin
AGENTS.md                         # one-shot agent runbook
plugins/
  tts/            hooks/ commands/ output-styles/ bin/ tts/
  notify/         hooks/ bin/
  sudo-askpass/   hooks/ bin/
  tmux-title/     hooks/
  w1am-skills/    skills/engineering/… skills/misc/…
```

Each plugin has its own `README.md` and `.claude-plugin/plugin.json`. The
marketplace `name` is `w1am`, so installs read `<plugin>@w1am` while the source
repo is `w1am/skills`.
