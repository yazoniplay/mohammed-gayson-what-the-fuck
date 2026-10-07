# Jack Pockets AutoVideo

Production-oriented open-source automation for fast-paced documentary video essays.

## Pipeline
topic -> script -> narration -> word alignment -> asset plan -> manifest -> Remotion render

## Features
- LLM-ready script generation with deterministic fallback
- ElevenLabs-ready narration stage
- faster-whisper word-level alignment
- beat-based story structure
- intensity-aware visual planning
- Pexels/provider adapter architecture
- captions and overlay contracts
- YouTube, Shorts, Square and 4K profiles
- GitHub Actions typecheck
- resumable run directories
- no secrets or downloaded media committed

## Quick start
```bash
npm install
python -m pip install -r requirements.txt
cp .env.example .env
npm run generate -- --topic "The strange history of abandoned malls"
```

Then use the generated manifest with Remotion.

> This project targets the broader fast-paced documentary/video-essay genre and does not attempt to clone one creator's exact signature style.
