# AutoVideo — Pro Documentary Engine

This is a high-end automated documentary editor: research/script planning, narration, word alignment, asset retrieval, edit planning, manifest generation, quality validation and Remotion rendering.

It is designed around the **general craft principles** of modern fast-paced documentary editing: aggressive pacing, editorial hierarchy, documentary evidence, kinetic typography, controlled camera motion, punchy transitions, sound-aware timing and visual variety.

It does **not** reproduce any creator's exact signature style or proprietary edit decisions.

## Run
```bash
npm install
python -m pip install -r requirements.txt
cp .env.example .env
npm run generate -- --topic "Why abandoned malls disappeared"
```

## Optional providers
OPENAI_API_KEY or ANTHROPIC_API_KEY, ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID, PEXELS_API_KEY, TAVILY_API_KEY.

The pipeline creates an editable run under `public/runs/<topic>/` and renders to `out/`.

## Production layers
- research grounding
- story beat architecture
- narration
- word-level timing
- asset search
- automatic edit planning
- captions
- overlays
- music ducking hook
- quality gate
- multi-format rendering

The renderer intentionally avoids bundled copyrighted media. Supply assets you have rights to use.
