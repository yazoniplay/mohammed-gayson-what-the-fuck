from __future__ import annotations
import json,os
from dotenv import load_dotenv
load_dotenv()

SYSTEM="""You are the editorial brain for an automated premium documentary editor.
Create an ORIGINAL factual long-form documentary plan. Do not imitate any named creator.

The normal finished video must be 8-14 minutes. Write enough real narration to support that duration:
target roughly 1,400-2,100 spoken words total (about 150 words/minute). Complex topics may naturally
expand toward 30 minutes, but never pad a story just to hit a runtime.

Use a strong narrative arc: cold-open, context, escalation, competing explanations/evidence, reveal,
fallout and ending. Make every beat advance the story. Every sentence should have a visual reason,
and factual claims should be specific enough to research.

Return ONLY valid JSON with 8-14 beats. Each beat needs narration, intensity 0-1, keywords, overlays
and a visual intent. Do not write placeholder narration, repeated filler, or generic one-line beats."""

def _normalize_plan(value,topic:str)->dict:
    if isinstance(value,list):
        return {"title":topic,"beats":value}
    if isinstance(value,dict):
        beats=value.get("beats")
        if isinstance(beats,list):
            value.setdefault("title",topic)
            return value
        for key in ("plan","script","sections","scenes"):
            candidate=value.get(key)
            if isinstance(candidate,list):
                return {"title":value.get("title",topic),"beats":candidate}
    raise ValueError("LLM returned an unsupported documentary plan shape")

def _gemini(topic:str)->dict:
    from google import genai
    from google.genai import types
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    r=client.models.generate_content(
        model=os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite",
        contents=f"{SYSTEM}\n\nBuild a complete long-form documentary plan about: {topic}",
        config=types.GenerateContentConfig(temperature=.7,response_mime_type="application/json"),
    )
    plan=_normalize_plan(json.loads(r.text),topic)
    words=sum(len(str(b.get("narration","")).split()) for b in plan["beats"])
    if words < 1200:
        raise ValueError(f"Gemini returned only {words} narration words; a long-form plan needs at least 1200")
    return plan

def _openai(topic:str)->dict:
    from openai import OpenAI
    c=OpenAI()
    r=c.chat.completions.create(
        model=os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":f"Build a complete long-form documentary plan about: {topic}"}],
        temperature=.7,
    )
    return _normalize_plan(json.loads(r.choices[0].message.content),topic)

def _anthropic(topic:str)->dict:
    from anthropic import Anthropic
    c=Anthropic()
    r=c.messages.create(
        model=os.getenv("ANTHROPIC_MODEL") or "claude-3-5-sonnet-latest",
        max_tokens=7000,system=SYSTEM,
        messages=[{"role":"user","content":f"Build a complete long-form documentary plan about: {topic}"}],
    )
    return _normalize_plan(json.loads(r.content[0].text),topic)

def generate(topic:str)->dict:
    provider=os.getenv("LLM_PROVIDER","auto").lower()
    order={"gemini":["gemini"],"openai":["openai"],"anthropic":["anthropic"],"auto":["gemini","openai","anthropic"]}.get(provider,["gemini","openai","anthropic"])
    for name in order:
        try:
            if name=="gemini" and os.getenv("GEMINI_API_KEY"): return _gemini(topic)
            if name=="openai" and os.getenv("OPENAI_API_KEY"): return _openai(topic)
            if name=="anthropic" and os.getenv("ANTHROPIC_API_KEY"): return _anthropic(topic)
        except Exception as exc:
            print(f"[llm] {name} failed: {exc}")
    from generate_script import fallback
    return fallback(topic)
