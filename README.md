# claude-plugins

A personal Claude Code marketplace. Each plugin is small and installs on its own —
take the ones you want.

## Add the marketplace

```
/plugin marketplace add w1am/claude-plugins
```

## Plugins

| Plugin | Type | What it does |
|--------|------|--------------|
| [`tts`](plugins/tts) | Stop hook + output style | Speaks each reply aloud through a fallback chain of TTS engines (`edge`, `kokoro`, `elevenlabs`), and ships a **Spoken** output style tuned for the ear. |
| [`notify`](plugins/notify) | Stop hook | Plays a short completion chime when a turn ends. |
| [`sudo-askpass`](plugins/sudo-askpass) | PreToolUse hook | Lets the Bash tool run `sudo` by routing the prompt through a GUI askpass helper. |
| [`tmux-title`](plugins/tmux-title) | Session hooks | Renames the tmux window to the project dir while Claude runs, restores it on exit. |
| [`dev-commands`](plugins/dev-commands) | Commands | `/session`, `/cut-release`, `/deepen`. |
| [`w1am-skills`](plugins/w1am-skills) | Skills | All personal skills in one plugin, organized by category (`skills/engineering/…`). Ships `naming-review`. |

Install any of them:

```
/plugin install tts@claude-plugins
/plugin install notify@claude-plugins
/plugin install sudo-askpass@claude-plugins
/plugin install tmux-title@claude-plugins
/plugin install dev-commands@claude-plugins
/plugin install w1am-skills@claude-plugins
```

## Layout

```
.claude-plugin/marketplace.json   # lists every plugin below
plugins/
  tts/            hooks/ commands/ output-styles/ bin/ tts/
  notify/         hooks/ bin/
  sudo-askpass/   hooks/ bin/
  tmux-title/     hooks/
  dev-commands/   commands/
  w1am-skills/    skills/engineering/…
```

Each plugin has its own `README.md` and `.claude-plugin/plugin.json`.
