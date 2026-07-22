# w1am/skills

A personal Claude Code marketplace (handle `w1am`). Each plugin is small and
installs on its own — take the ones you want.

## Add the marketplace

```
/plugin marketplace add w1am/skills
```

## Plugins

| Plugin | Type | What it does |
|--------|------|--------------|
| [`tts`](plugins/tts) | Stop hook + output style | Speaks each reply aloud through a fallback chain of TTS engines (`edge`, `kokoro`, `elevenlabs`), and ships a **Spoken** output style tuned for the ear. |
| [`notify`](plugins/notify) | Stop hook | Plays a short completion chime when a turn ends. |
| [`sudo-askpass`](plugins/sudo-askpass) | PreToolUse hook | Lets the Bash tool run `sudo` by routing the prompt through a GUI askpass helper. |
| [`tmux-title`](plugins/tmux-title) | Session hooks | Renames the tmux window to the project dir while Claude runs, restores it on exit. |
| [`w1am-skills`](plugins/w1am-skills) | Skills | All personal skills in one plugin, organized by category. Each runs as a `/command`: `/naming-review`, `/deepen`, `/cut-release`, `/session`. |

Install any of them:

```
/plugin install tts@w1am
/plugin install notify@w1am
/plugin install sudo-askpass@w1am
/plugin install tmux-title@w1am
/plugin install w1am-skills@w1am
```

## Layout

```
.claude-plugin/marketplace.json   # lists every plugin below
plugins/
  tts/            hooks/ commands/ output-styles/ bin/ tts/
  notify/         hooks/ bin/
  sudo-askpass/   hooks/ bin/
  tmux-title/     hooks/
  w1am-skills/    skills/engineering/… skills/misc/…
```

Each plugin has its own `README.md` and `.claude-plugin/plugin.json`.
