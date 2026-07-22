# skills

A single plugin holding all personal skills. Add a new skill by dropping a
`skills/<name>/SKILL.md` into this plugin — no new plugin needed.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install skills@claude-plugins
```

## Skills

| Skill | What it does |
|-------|--------------|
| `naming-review` | Reviews names in recently-changed code across two lenses — drift (a name that stopped matching what it holds) and simplicity (a name that was never the plainest fit) — and recommends deleting or splitting a symbol when no rename can fix it. Triggers on "review vocab", "check naming", "this name bothers me", or after any rename or refactor. |
