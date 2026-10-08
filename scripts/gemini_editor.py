from __future__ import annotations
import json,os
from google import genai
from google.genai import types

SYSTEM="""You are a senior documentary post-production editor.
Given a documentary beat, act as the final picture editor. Do not imitate any named creator. Optimize for clarity, pacing, evidence, visual variety, emotional rhythm and deliberate emphasis. Return JSON only. Plan sentence-level editorial decisions: intent, cut priority, important words, visual role, composition, camera motion, overlay, and whether an SFX accent is justified. Prefer motivated cuts over effects. Never use an effect just because it is available. Avoid repeating the same composition twice in a row. Visual roles include archival photo, document, screenshot, map, chart, quote card, headline, texture and full-bleed B-roll."""

def refine_beat(beat:dict)->dict:
    if not os.getenv("GEMINI_API_KEY"): return beat
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt=json.dumps({"title":beat.get("title",""),"narration":beat.get("narration",""),"keywords":beat.get("keywords",[]),"intensity":beat.get("intensity",.5),"research":beat.get("research",[])[:4]},ensure_ascii=False)
    try:
        r=client.models.generate_content(
            model=os.getenv("GEMINI_EDITOR_MODEL",os.getenv("GEMINI_MODEL","gemini-3.5-flash-lite")),
            contents=f"{SYSTEM}\n\nBeat:\n{prompt}",
            config=types.GenerateContentConfig(temperature=.35,response_mime_type="application/json"),
        )
        data=json.loads(r.text)
        beat["editorial"]=data
        if data.get("keywords"): beat["keywords"]=data["keywords"][:8]
    except Exception as exc:
        print(f"[gemini-editor] refinement skipped: {exc}")
    return beat
