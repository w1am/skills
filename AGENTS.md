# AGENTS.md

This repository is a Claude Code plugin marketplace designed to be operated by an
autonomous agent from these docs alone. You have shell access. Nothing here needs
the interactive `/plugin` TUI — use the `claude plugin` CLI.

## Facts you need

- Marketplace name: `w1am`. Source repo: `w1am/skills`. Install ids: `<plugin>@w1am`.
- Plugins: `tts`, `notify`, `sudo-askpass`, `tmux-title`, `w1am-skills`.
- After `claude plugin marketplace add`, the repo is cloned to
  `~/.claude/plugins/marketplaces/w1am/`, so any shipped script is under
  `~/.claude/plugins/marketplaces/w1am/plugins/<plugin>/…`.
- Requires the `claude` CLI on `PATH` (`claude --version`). Plugin CLI is
  available from Claude Code 2.1.x.

## Install everything

```sh
claude plugin marketplace add w1am/skills
for p in tts notify sudo-askpass tmux-title w1am-skills; do
  claude plugin install "$p@w1am" --scope user
done
claude plugin list
```

## Per-plugin setup and verification

```sh
# tts — install the default engine (edge-tts via uv) and confirm it can speak.
tts_bin="$(dirname "$(find ~/.claude/plugins/marketplaces/w1am -path '*/tts/bin/setup.sh' | head -1)")"
bash "$tts_bin/setup.sh"            # add --kokoro for the offline engine
"$tts_bin/claude-tts" doctor        # shows the engine chain and audio player
"$tts_bin/claude-tts" say "ready"   # optional smoke test

# sudo-askpass — verify the hook rewrites a sudo command (no sudo actually runs).
hook="$(find ~/.claude/plugins/marketplaces/w1am -path '*/sudo-askpass/bin/sudo-hook.py' | head -1)"
echo '{"tool_name":"Bash","tool_input":{"command":"sudo true"}}' | python3 "$hook"

# notify — play the chime once.
bash "$(find ~/.claude/plugins/marketplaces/w1am -path '*/notify/bin/notify.sh' | head -1)"

# tmux-title, w1am-skills — no setup; active/available after install.
```

## System prerequisites (install as needed for the target OS)

- `tts`: `python3`, an audio player (`mpv` / `ffplay` / `paplay` / `afplay`), network for `edge`.
- `notify`: `paplay` (Linux) or `afplay` (macOS).
- `sudo-askpass`: `zenity` (Linux) for the password dialog.
- `w1am-skills` `/session`: a clipboard tool (`wl-copy` / `xclip` / `xsel` / `pbcopy`).

## Manage

```sh
claude plugin marketplace update w1am
claude plugin update <plugin>@w1am
claude plugin uninstall <plugin>@w1am
claude plugin marketplace remove w1am
```

Each plugin's `README.md` holds its full config surface (env vars, files). Skill
bodies under `plugins/w1am-skills/skills/**/SKILL.md` are self-contained
instructions you can follow directly.
