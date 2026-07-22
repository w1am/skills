# tts

Speak Claude Code's replies aloud. Ships:

- a **Stop hook** that reads each reply and speaks it,
- a fallback **chain of TTS engines** — `edge` (free, no key), `kokoro` (offline), `elevenlabs` (best quality, metered),
- a **Spoken** output style that makes replies sound right for the ear instead of the screen.

The hook extracts the `<speak>…</speak>` block the Spoken style emits. Without that style it falls back to speaking the first paragraph, so it still works before you switch styles.

## Install

```
/plugin marketplace add w1am/claude-plugins
/plugin install tts@claude-plugins
```

Then set up the engine and pick the voice style:

```
/tts-setup
/output-style Spoken
```

`/tts-setup` installs `edge-tts` as a global [uv](https://docs.astral.sh/uv/) tool (the zero-config default), installing uv first if needed. It needs `python3` and an audio player on `PATH`.

### Audio player (one system dependency)

Playback uses the first of these it finds: `mpv`, `afplay` (macOS), `ffplay` (ffmpeg), `paplay`, `aplay`. Install one, e.g. `brew install mpv` or `sudo apt install mpv`.

## Engines

| Engine | Setup | Notes |
|--------|-------|-------|
| `edge` | `/tts-setup` (uv tool, default) | Free, no key, needs network. Default voice. |
| `kokoro` | `/tts-setup --kokoro` | Offline, ~350MB model, better voice. |
| `elevenlabs` | put key in `~/.claude/.elevenlabs-key` or `ELEVENLABS_API_KEY` | Best quality, metered. |

Default chain is `edge, kokoro, elevenlabs` — it uses the first one that's ready. Reorder with `CC_TTS_CHAIN`, or pin one with `CC_TTS_ENGINE`.

## Check it works

```
${CLAUDE_PLUGIN_ROOT}/bin/claude-tts doctor      # show chain, player, per-engine status
${CLAUDE_PLUGIN_ROOT}/bin/claude-tts say hello    # speak a test phrase
```

## Configuration (env vars)

| Var | Default | Effect |
|-----|---------|--------|
| `CC_TTS_ENGINE` | — | Pin a single engine, ignore the chain. |
| `CC_TTS_CHAIN` | `edge,kokoro,elevenlabs` | Comma-separated fallback order. |
| `CC_TTS_MAX_CHARS` | `2000` | Truncate longer replies. |
| `CC_TTS_IGNORE_MEDIA` | — | Speak even while other media is playing. |
| `CC_TTS_VOICE` / `CC_TTS_RATE` / `CC_TTS_PITCH` | Edge voice knobs. |
| `CC_TTS_KOKORO_VOICE` / `CC_TTS_KOKORO_SPEED` | Kokoro voice knobs. |
| `CC_TTS_EL_VOICE` / `CC_TTS_EL_MODEL` | ElevenLabs voice knobs. |
| `CC_TTS_DEBUG=1` | — | Log to `~/.claude/tts.log`. |

List available voices per engine:

```
${CLAUDE_PLUGIN_ROOT}/bin/claude-tts voices -e edge -u
${CLAUDE_PLUGIN_ROOT}/bin/claude-tts audition -e edge en-IE-EmilyNeural en-GB-SoniaNeural
```

## How it works

`hooks/hooks.json` registers a Stop hook → `bin/speak.sh`. That script skips if other audio is playing, takes a single-speaker lock, and pipes the reply into `bin/claude-tts speak`. The Python package (`tts/`) extracts and cleans the spoken text, then walks the engine chain until one synthesizes audio, and plays it.
