# w1am-skills

All personal agent skills in one plugin, organized by category the way
[mattpocock/skills](https://github.com/mattpocock/skills) does it: each skill is
a folder with a `SKILL.md`, grouped under a category directory with its own
`README.md`, and every skill is listed explicitly in the manifest (category
subfolders aren't auto-discovered).

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install w1am-skills@w1am
```

## Layout

```
skills/
  engineering/
    README.md
    naming-review/
      SKILL.md
```

Add a skill by dropping `skills/<category>/<name>/SKILL.md` in and adding its
folder to the `skills` array in `.claude-plugin/plugin.json`.

## Skills

### Engineering

| Skill | What it does |
|-------|--------------|
| [`naming-review`](skills/engineering/naming-review/SKILL.md) | Reviews names in changed code for drift and simplicity; recommends deleting or splitting a symbol when no rename fits. |
