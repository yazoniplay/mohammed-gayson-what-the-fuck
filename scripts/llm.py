from __future__ import annotations
import json,os
from dotenv import load_dotenv
load_dotenv()

SYSTEM="""You are the editorial brain for an automated premium documentary editor.
Create original factual documentary plans with a strong narrative arc. Think like a senior editor:
every sentence must have a visual reason, evidence must feel tangible, reveals must escalate, and
the screen should change when the information changes. Use cold-open, context, escalation, reveal,
fallout and ending beats. Return ONLY valid JSON with 8-14 beats. The normal target is 8-14 minutes; complex topics may expand toward 30 minutes when genuinely necessary. Each beat needs narration,
intensity 0-1, keywords, overlays and a visual intent. Do not imitate a named creator's exact style."""

def _gemini(topic:str)->dict:
    from google import genai
    from google.genai import types
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    r=client.models.generate_content(
        model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),
        contents=f"{SYSTEM}\n\nBuild a fast-paced documentary video plan about: {topic}",
        config=types.GenerateContentConfig(
            temperature=.7,
            response_mime_type="application/json",
        ),
    )
    return json.loads(r.text)

def _openai(topic:str)->dict:
    from openai import OpenAI
    c=OpenAI()
    r=c.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        response_format={"type":"json_object"},
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":f"Build a fast-paced documentary video plan about: {topic}"}],
        temperature=.7,
    )
    return json.loads(r.choices[0].message.content)

def _anthropic(topic:str)->dict:
    from anthropic import Anthropic
    c=Anthropic()
    r=c.messages.create(
        model=os.getenv("ANTHROPIC_MODEL","claude-3-5-sonnet-latest"),
        max_tokens=5000,system=SYSTEM,
        messages=[{"role":"user","content":f"Build a fast-paced documentary video plan about: {topic}"}],
    )
    return json.loads(r.content[0].text)

def generate(topic:str)->dict:
    # Gemini is first-class, with explicit provider selection and safe fallback.
    provider=os.getenv("LLM_PROVIDER","auto").lower()
    order={"gemini":["gemini"],"openai":["openai"],"anthropic":["anthropic"],"auto":["gemini","openai","anthropic"]}.get(provider,["gemini","openai","anthropic"])
    for name in order:
        try:
            if name=="gemini" and os.getenv("GEMINI_API_KEY"): return _gemini(topic)
            if name=="openai" and os.getenv("OPENAI_API_KEY"): return _openai(topic)
            if name=="anthropic" and os.getenv("ANTHROPIC_API_KEY"): return _anthropic(topic)
        except Exception as exc:
            print(f"[llm] {name} failed: {exc}")
    from generate_script import fallback_plan
    return fallback_plan(topic)
