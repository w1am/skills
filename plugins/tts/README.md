# tts

Speak Claude Code's replies aloud. Ships a **Stop hook** that reads each reply, a
fallback **chain of TTS engines** — `say` (macOS native, offline), `edge` (free,
no key), `kokoro` (offline), `elevenlabs` (best quality, metered) — and a
**Spoken** output style that makes replies sound right for the ear.

The hook extracts the `<speak>…</speak>` block the Spoken style emits. Without
that style it falls back to speaking the first paragraph.

## Install (agent, shell)

```sh
claude plugin marketplace add w1am/skills
claude plugin install tts@w1am --scope user
```

## Setup (required, one step)

The engine isn't bundled; a setup script installs it. Locate and run it:

```sh
tts_bin="$(dirname "$(find ~/.claude/plugins/marketplaces/w1am -path '*/tts/bin/setup.sh' | head -1)")"
bash "$tts_bin/setup.sh"            # default: edge-tts as a global uv tool
bash "$tts_bin/setup.sh" --kokoro  # optional: offline engine + ~350MB model
```

`setup.sh` installs [uv](https://docs.astral.sh/uv/) if missing, then `edge-tts`.
It needs `python3` and, on Linux, an audio player on `PATH`.

**Windows:** run `setup.sh` from **Git Bash** (bundled with Git for Windows,
which Claude Code already uses on Windows). Everything else works the same. uv is
installed via its PowerShell installer automatically.

### Audio player

Playback uses the first found of: `mpv`, `afplay` (macOS), `ffplay` (ffmpeg),
`paplay`, `pw-play`, `aplay`, `cvlc`. macOS ships `afplay`, so nothing to
install. Windows falls back to a built-in PowerShell player (Windows Media via
`winmm`), so nothing to install there either. On Linux install one, e.g.
`sudo apt install mpv`.

## Verify (agent, shell)

```sh
"$tts_bin/claude-tts" doctor          # engine chain, player, per-engine status
"$tts_bin/claude-tts" say "hello"     # speak a test phrase
```

Then select the voice output style for speech-tuned replies. In a Claude Code
session: `/output-style Spoken`, or set `"outputStyle": "Spoken"` in settings.

## Engines

| Engine | Setup | Notes |
|--------|-------|-------|
| `say` | none (macOS built-in) | Offline, instant, no download. macOS only. |
| `edge` | `setup.sh` (uv tool, default) | Free, no key, needs network. Default voice. |
| `kokoro` | `setup.sh --kokoro` | Offline, ~350MB model, better voice. |
| `elevenlabs` | key in `~/.claude/.elevenlabs-key` or `ELEVENLABS_API_KEY` | Best quality, metered. |

The default chain is OS-specific — the first ready engine wins:

- **macOS**: `say, edge, kokoro, elevenlabs` (native `say` first: zero-install, offline).
- **Linux / Windows**: `edge, kokoro, elevenlabs`.

Reorder with `CC_TTS_CHAIN`; a single value pins one engine (`CC_TTS_CHAIN=kokoro`).
`say` is offline and instant but a touch less natural than `kokoro`; pin or reorder
if you want Kokoro's quality on macOS.

## Configuration (env vars)

Set these in the Claude Code environment (e.g. `env` in settings.json) to change
behavior:

| Var | Default | Effect |
|-----|---------|--------|
| `CC_TTS_CHAIN` | per-OS (see above) | Comma-separated fallback order; a single value pins one engine. |
| `CC_TTS_MAX_CHARS` | `2000` | Truncate longer replies. |
| `CC_TTS_TIMEOUT` | per-engine | Override synthesis timeout (seconds) for every engine. |
| `CC_TTS_IGNORE_MEDIA` | — | Speak even while other media is playing (Linux only). |
| `CC_TTS_EDGE_VOICE` / `CC_TTS_EDGE_RATE` / `CC_TTS_EDGE_PITCH` | | Edge voice knobs. |
| `CC_TTS_SAY_VOICE` / `CC_TTS_SAY_RATE` | | macOS `say` voice and words-per-minute. |
| `CC_TTS_KOKORO_VOICE` / `CC_TTS_KOKORO_SPEED` | | Kokoro voice knobs. |
| `CC_TTS_EL_VOICE` / `CC_TTS_EL_MODEL` | | ElevenLabs voice knobs. |
| `CC_TTS_DEBUG=1` | — | Log to `~/.claude/tts.log`. |

List available voices per engine:

```sh
"$tts_bin/claude-tts" voices -e edge -u
"$tts_bin/claude-tts" audition -e edge en-IE-EmilyNeural en-GB-SoniaNeural
```

## How it works

`hooks/hooks.json` registers a Stop hook that runs `bin/speak.sh` via `bash`
(portable across Linux, macOS, and Windows Git Bash). The launcher pipes the
reply into `bin/claude-tts speak`, which returns immediately after spawning a
detached worker. The Python package (`tts/`) does the cross-platform work:
skip if other audio is playing (Linux MPRIS), take a single-speaker lock
(`fcntl`/`msvcrt`), extract and clean the spoken text, walk the engine chain
until one synthesizes audio, and play it.
