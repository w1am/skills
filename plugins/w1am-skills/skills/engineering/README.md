# Engineering

Skills for code work.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[deepen](./deepen/SKILL.md)** — `/deepen [target]`. Simplify code by simplifying the business logic and model, not by extracting helpers. Fans out parallel sub-agents to find a hidden concept or better model, presents the synthesis, then applies it only after you confirm.
- **[cut-release](./cut-release/SKILL.md)** — `/cut-release <new> [prev] [--style customers|developers|internal]`. Write release notes for a version range and update the GitHub draft release, with a verify pass before publishing.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[naming-review](./naming-review/SKILL.md)** — Reviews names in recently-changed code across two lenses: drift (a name that stopped matching what it holds) and simplicity (a name that was never the plainest fit). Recommends deleting or splitting a symbol when no rename can fix it. Triggers on "review vocab", "check naming", "this name bothers me", or after any rename or refactor.
