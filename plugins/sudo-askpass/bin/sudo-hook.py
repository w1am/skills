#!/usr/bin/env python3
"""PreToolUse hook: route sudo through a native GUI askpass helper.

Claude Code's Bash tool has no interactive tty, so `sudo` normally fails with
"a terminal is required to read the password". This hook rewrites any
command-position `sudo` into `SUDO_ASKPASS=<helper> sudo -A ...`, so sudo asks
for the password via the GUI helper instead of a tty.

It does NOT set permissionDecision, so Claude Code's normal permission prompt
for the (rewritten) command still applies.

When a sudo command opts out (-n/-A) the rewrite is skipped, but the hook still
reports that askpass exists, so a failing probe is not misread as "no sudo here".
"""
import json
import os
import re
import sys

HELPER = os.environ.get("CC_SUDO_ASKPASS") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sudo-askpass.sh"
)

# `sudo` only when it starts a command: at the very start, or right after a
# shell separator/opening paren. Avoids matching `sudo` inside strings/args.
SUDO_AT_CMD = re.compile(r"(^|[\n;&|(]\s*)\bsudo\b")


def shquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


REWROTE = "sudo rewritten to prompt for the password via the native GUI askpass helper."
OPTED_OUT = (
    "sudo IS available here: a PreToolUse hook supplies the password via a GUI askpass "
    "helper. This command used -n/-A, which opts out of that rewrite, so a failure means "
    "'no cached credentials', NOT 'sudo unavailable'. Do not conclude sudo is unusable "
    "from this result. Re-run the real command without -n and let the helper handle it."
)


def rewrite(cmd):
    changed = opted_out = False

    def repl(m):
        nonlocal changed, opted_out
        following = re.split(r"[\n;&|]", cmd[m.end():], maxsplit=1)[0]
        # leave alone if the user already chose askpass (-A) or no-prompt (-n)
        if re.search(r"(^|\s)-A(\s|$)", following) or re.search(r"(^|\s)-n(\s|$)", following):
            opted_out = True
            return m.group(0)
        changed = True
        return f"{m.group(1)}SUDO_ASKPASS={shquote(HELPER)} sudo -A"

    new = SUDO_AT_CMD.sub(repl, cmd)
    return (new if changed else None), opted_out


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") != "Bash":
        return
    tool_input = data.get("tool_input") or {}
    cmd = tool_input.get("command")
    if not isinstance(cmd, str) or "sudo" not in cmd:
        return

    new, opted_out = rewrite(cmd)
    if new is None and not opted_out:
        return

    out = {"hookEventName": "PreToolUse"}
    if new is None:
        out["additionalContext"] = OPTED_OUT
    else:
        out["updatedInput"] = {**tool_input, "command": new}
        out["additionalContext"] = REWROTE

    json.dump({"hookSpecificOutput": out}, sys.stdout)


if __name__ == "__main__":
    main()
