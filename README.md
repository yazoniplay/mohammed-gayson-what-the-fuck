# Jack Pockets AutoVideo

A full topic-to-video documentary automation pipeline.

## One command

```bash
npm install
python -m pip install -r requirements.txt
cp .env.example .env
npm run generate -- --topic "The strange history of abandoned malls"
```

With API keys configured, this pipeline performs:

1. LLM script planning
2. ElevenLabs narration
3. faster-whisper word timestamps
4. Pexels visual acquisition
5. typed manifest construction
6. Remotion rendering
7. MP4 output in `out/`

Use `--no-render` to stop after manifest creation.

### Environment

Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, and optionally `PEXELS_API_KEY`.

The system falls back to a deterministic script when no LLM key exists, but real narration requires ElevenLabs.

### Profiles

`youtube` 1920x1080, `shorts` 1080x1920, `square` 1080x1080, `4k` 3840x2160.

Downloaded media and generated runs live under ignored `public/runs` and are never committed.

This project implements a broad fast-paced documentary/video-essay grammar rather than copying any one creator's exact signature style.
