---
name: session
description: Copy the current Claude Code session id to the clipboard. Run it as /session.
disable-model-invocation: true
allowed-tools: Bash
---

Copy the current session id to the clipboard, then confirm. Run exactly this, once:

```
printf '%s' "$CLAUDE_CODE_SESSION_ID" | { wl-copy 2>/dev/null || xclip -selection clipboard 2>/dev/null || xsel -ib 2>/dev/null || pbcopy 2>/dev/null; } && printf '%s' "$CLAUDE_CODE_SESSION_ID"
```

Tell the user the printed session id was copied to their clipboard. Do nothing else.
