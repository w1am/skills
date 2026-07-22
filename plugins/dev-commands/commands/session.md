---
description: Copy the current session id to the clipboard
allowed-tools: Bash(printf:*), Bash(wl-copy:*), Bash(xclip:*), Bash(xsel:*), Bash(pbcopy:*)
---

Session id copied to clipboard: !`printf '%s' "$CLAUDE_CODE_SESSION_ID" | { wl-copy 2>/dev/null || xclip -selection clipboard 2>/dev/null || xsel -ib 2>/dev/null || pbcopy 2>/dev/null; } && printf '%s' "$CLAUDE_CODE_SESSION_ID"`

Confirm to the user that the session id above was copied to their clipboard. Do not do anything else.
