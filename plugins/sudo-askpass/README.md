# sudo-askpass

Claude Code's Bash tool has no interactive tty, so `sudo` normally fails with
"a terminal is required to read the password". This plugin's PreToolUse hook
rewrites any command-position `sudo` into `SUDO_ASKPASS=<helper> sudo -A …`, so
sudo asks for the password through a GUI dialog instead of a tty.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install sudo-askpass@claude-plugins
```

## Requirements

- Linux with `zenity` for the password dialog (the default helper).
- macOS or other setups: point `CC_SUDO_ASKPASS` at your own helper (see below).

## How it works

`hooks/hooks.json` registers a PreToolUse (Bash) hook → `bin/sudo-hook.py`. It
rewrites `sudo` at a command position and sets `SUDO_ASKPASS` to
`bin/sudo-askpass.sh`, which pops a `zenity` password dialog and prints the
password to sudo on stdout.

The hook does **not** set a permission decision, so Claude Code's normal
permission prompt for the rewritten command still applies. A `sudo` that opts out
with `-n`/`-A` is left untouched, and the hook reports that askpass exists so a
failing probe is not misread as "no sudo here".

## Configuration

| Var | Effect |
|-----|--------|
| `CC_SUDO_ASKPASS` | Absolute path to a custom askpass helper. Defaults to the bundled `sudo-askpass.sh`. |

The helper contract (imposed by `sudo -A`): print the password to stdout and exit
0, or print nothing and exit non-zero to abort.
