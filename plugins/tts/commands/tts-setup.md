---
name: tts-setup
description: Interactive claude-tts setup — detects your OS and asks which voices, player, and output style you want
---

Run a **full interactive setup** for the `tts` plugin. Detect the OS, ask the user what they want with `AskUserQuestion`, install only that, persist their choices, and verify. Follow the steps in order. Do not install anything before asking, and do not skip the questions.

## 1. Detect platform and current state

Run both:

```
uname -s
bash "${CLAUDE_PLUGIN_ROOT}/bin/claude-tts" doctor
```

Map `uname -s`: `Darwin` → macOS, `Linux` → Linux, `MINGW*`/`MSYS*`/`CYGWIN*` → Windows (Git Bash). From `doctor`, note which engines already show `ready`, the resolved chain, and whether an audio player was found. On Windows every `bash` command below must run under Git Bash (Claude Code already uses it there).

## 2. Ask which engines to set up

Use `AskUserQuestion`, `multiSelect: true`, `header: "Engines"`. Show **only** the options for the detected OS. Append " — already ready" to any engine `doctor` already reported ready, and put the recommended one first.

**macOS** (four options):
- `say` — native macOS voice. Offline, instant, zero install. *(Recommended)*
- `edge` — free Microsoft voice, needs network, more natural than `say`. *(Recommended)*
- `kokoro` — offline neural voice, best offline quality, ~350MB download.
- `elevenlabs` — top quality, needs an API key, metered.

**Linux / Windows** (three options):
- `edge` — free Microsoft voice, needs network. *(Recommended)*
- `kokoro` — offline neural voice, ~350MB download.
- `elevenlabs` — top quality, needs an API key, metered.

## 3. Install the chosen engines

- If `edge` **or** `kokoro` was chosen, run the setup script (add `--kokoro` only when `kokoro` was chosen — it installs `edge` too as the free base):
  ```
  bash "${CLAUDE_PLUGIN_ROOT}/bin/setup.sh"            # edge
  bash "${CLAUDE_PLUGIN_ROOT}/bin/setup.sh" --kokoro   # edge + offline kokoro (~350MB)
  ```
- `say` needs nothing installed — it ships with macOS.
- If `elevenlabs` was chosen, ask the user conversationally (not a multiple-choice question) for their ElevenLabs API key. If they paste it, write it to `~/.claude/.elevenlabs-key` and `chmod 600` that file. If they decline, tell them to set `ELEVENLABS_API_KEY` or drop the key in that file later.

## 4. Audio player (Linux only)

macOS ships `afplay` and Windows has a built-in player, so skip this on those. On Linux, only if `doctor` reported no player, use `AskUserQuestion` (`header: "Player"`) to pick one, then install it with the system package manager:
- `mpv` *(Recommended)* → `sudo apt install -y mpv` (or the distro equivalent)
- `ffmpeg` — provides `ffplay`
- `pulseaudio-utils` — provides `paplay`

## 5. Set the default voice

The first ready engine in the chain wins. This matters on macOS: the built-in default puts `say` first, so if the user set up `edge`/`kokoro`/`elevenlabs` and wants one of those to speak by default, the chain must be reordered.

If the user ended up with **more than one** ready engine, use `AskUserQuestion` (`header: "Default"`, single select) listing their ready engines and asking which should speak first. Then offer to persist it by adding `CC_TTS_CHAIN` (their pick first, the others as fallback, e.g. `edge,say,elevenlabs`) to the `env` block of `~/.claude/settings.json`. If they set up only one engine, or their preference already matches the resolved chain from step 1, skip this.

## 6. Enable the Spoken output style

Use `AskUserQuestion` (`header: "Output style"`, yes/no) asking whether to tune replies for speech now. If yes, add `"outputStyle": "Spoken"` to `~/.claude/settings.json`, and mention they can also toggle it any time with `/output-style Spoken`.

## 7. Verify

Re-run doctor and report, in one or two lines, which engines are ready, the resolved default, and the player:

```
bash "${CLAUDE_PLUGIN_ROOT}/bin/claude-tts" doctor
```

Then offer a quick test they can confirm by ear:

```
bash "${CLAUDE_PLUGIN_ROOT}/bin/claude-tts" say "Setup complete."
```
