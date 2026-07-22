# naming-review

A skill that reviews names in recently-changed code. It reads two lenses —
**drift** (a name that stopped matching what it holds) and **simplicity** (a name
that was never the plainest fit) — and will recommend deleting or splitting a
symbol when no rename can fix it.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install naming-review@claude-plugins
```

## Use

The skill triggers on prompts like "review vocab", "check naming", "are these
names consistent", "this name bothers me", or after any rename or refactor. It
proposes concrete changes and preserves behavior.
