# AutoVideo — Editorial Brain

An automated documentary editor built around editorial decisions rather than slideshow assembly.

The system uses narration as the timeline backbone, classifies each sentence, selects a visual intent, creates shot boundaries, builds layered compositions, and validates the resulting timeline before rendering.

It targets the broad craft of modern fast-paced documentary/video-essay editing: evidence-led visuals, kinetic typography, punch-ins, annotations, controlled transitions, deliberate reveals and sound-aware rhythm. It does not reproduce any named creator's exact signature style.

## Pipeline

TOPIC → RESEARCH → STORY → NARRATION → WORD ALIGNMENT → EDITORIAL BRAIN → ASSET PLAN → SHOT PLAN → QUALITY GATE → REMOTION

## Run

```bash
npm install
python -m pip install -r requirements.txt
cp .env.example .env
npm run generate -- --topic "Why abandoned malls disappeared"
```

## Profiles

```bash
npm run generate -- --topic "..." --profile youtube
npm run generate -- --topic "..." --profile shorts
npm run generate -- --topic "..." --profile square
npm run generate -- --topic "..." --profile 4k
```

Optional providers: OPENAI_API_KEY or ANTHROPIC_API_KEY, ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID, PEXELS_API_KEY and TAVILY_API_KEY.

No copyrighted media is bundled. Use assets you have rights to use.
