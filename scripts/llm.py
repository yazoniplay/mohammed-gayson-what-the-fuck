from __future__ import annotations
import json, os
from typing import Any
from dotenv import load_dotenv
load_dotenv()

SYSTEM = """You are a documentary video producer. Build factual, original, punchy video-essay scripts.
Return ONLY valid JSON. Use 6-10 beats: cold-open, context, escalation, reveal, fallout, ending.
Each beat has kind, narration, intensity (0-1), keywords (array), overlays (array of objects with type/text).
Avoid unsupported claims; when the topic needs research, phrase uncertain facts cautiously."""

def generate(topic:str)->dict[str,Any]:
    prompt=f"Create a 2-4 minute documentary video plan about: {topic}"
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        r=OpenAI().chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
          response_format={"type":"json_object"},messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}],temperature=.8)
        return json.loads(r.choices[0].message.content)
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        r=Anthropic().messages.create(model=os.getenv("ANTHROPIC_MODEL","claude-3-5-sonnet-latest"),
          max_tokens=5000,system=SYSTEM,messages=[{"role":"user","content":prompt}])
        return json.loads(r.content[0].text)
    from generate_script import fallback
    return fallback(topic)
