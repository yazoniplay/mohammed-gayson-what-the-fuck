from __future__ import annotations
import json,os
from google import genai
from google.genai import types

SYSTEM="""You are a senior documentary post-production editor.
Given a documentary beat, return JSON describing editorial decisions. Do not imitate any named
creator. Optimize for clarity, pacing, evidence, visual variety and deliberate emphasis.
Choose between setup, evidence, explain, contrast, reveal, consequence and punchline.
For each sentence identify important words and recommend visual roles such as archival photo,
document, screenshot, map, chart, quote card or texture. Avoid random effects."""

def refine_beat(beat:dict)->dict:
    if not os.getenv("GEMINI_API_KEY"): return beat
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt=json.dumps({"narration":beat.get("narration",""),"keywords":beat.get("keywords",[]),"intensity":beat.get("intensity",.5)},ensure_ascii=False)
    try:
        r=client.models.generate_content(
            model=os.getenv("GEMINI_EDITOR_MODEL",os.getenv("GEMINI_MODEL","gemini-2.5-flash")),
            contents=f"{SYSTEM}\n\nBeat:\n{prompt}",
            config=types.GenerateContentConfig(temperature=.35,response_mime_type="application/json"),
        )
        data=json.loads(r.text)
        beat["editorial"]=data
        if data.get("keywords"): beat["keywords"]=data["keywords"][:8]
    except Exception as exc:
        print(f"[gemini-editor] refinement skipped: {exc}")
    return beat
