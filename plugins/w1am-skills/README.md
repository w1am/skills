# w1am-skills

All personal agent skills in one plugin, organized by category the way
[mattpocock/skills](https://github.com/mattpocock/skills) does it: each skill is
a folder with a `SKILL.md`, grouped under a category directory, and every skill
is listed explicitly in the manifest (category subfolders aren't
auto-discovered).

## Install (agent, shell)

```sh
claude plugin marketplace add w1am/skills
claude plugin install w1am-skills@w1am --scope user
```

Available immediately, no setup. Each skill is invocable as a `/command` (its
name; plugin skills also autocomplete as `/w1am-skills:<name>`). Ones with rich
trigger phrasing may also be model-invoked; the rest set
`disable-model-invocation: true` so they run only when asked.

Every `SKILL.md` is self-contained: an agent can read the raw file and follow it
directly without invoking the plugin. The bodies use command-style features —
`argument-hint`, `$ARGUMENTS`, and `` !`command` `` shell injection — which work
because Claude Code merged custom commands into skills.

## Layout

```
skills/
  engineering/
    naming-review/   SKILL.md
    deepen/          SKILL.md
    cut-release/     SKILL.md
  misc/
    session/         SKILL.md
```

Add a skill by dropping `skills/<category>/<name>/SKILL.md` in and adding its
folder to the `skills` array in `.claude-plugin/plugin.json`.

## Skills

### Engineering

| Skill | Run | What it does |
|-------|-----|--------------|
| [`naming-review`](skills/engineering/naming-review/SKILL.md) | model or `/naming-review` | Reviews names in changed code for drift and simplicity; recommends deleting or splitting a symbol when no rename fits. |
| [`deepen`](skills/engineering/deepen/SKILL.md) | `/deepen [target]` | Simplify the business logic and model, not just the code — fan out sub-agents to find a hidden concept, then apply after you confirm. |
| [`cut-release`](skills/engineering/cut-release/SKILL.md) | `/cut-release <new> [prev]` | Write release notes for a version range and update the GitHub draft release. |

### Misc

| Skill | Run | What it does |
|-------|-----|--------------|
| [`session`](skills/misc/session/SKILL.md) | `/session` | Copy the current session id to the clipboard. |
