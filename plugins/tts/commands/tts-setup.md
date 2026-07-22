---
name: tts-setup
description: Install the claude-tts Python environment (edge-tts by default, add --kokoro for the offline voice)
---

Run the tts setup script to install the default engine (`edge-tts` as a global uv tool; `--kokoro` additionally builds an offline venv):

```
${CLAUDE_PLUGIN_ROOT}/bin/setup.sh
```

If the user asked for the offline Kokoro voice, run it with the `--kokoro` flag instead (this also downloads a ~350MB model):

```
${CLAUDE_PLUGIN_ROOT}/bin/setup.sh --kokoro
```

After it finishes, the script prints `claude-tts doctor` output. Report whether an engine is ready and whether an audio player was found. If no player was found, tell the user to install one of: mpv, ffmpeg (ffplay), or pulseaudio (paplay).

Then remind the user to select the voice output style with `/output-style Spoken` if they want replies tuned for speech.
