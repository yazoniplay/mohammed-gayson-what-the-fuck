from __future__ import annotations
import json
from pathlib import Path
from editorial_brain import build_shots
def build(plan,audio_src,words,assets_by_beat,profile,out):
    beats=[];cursor=0.0
    for i,b in enumerate(plan["beats"]):
        narration=str(b.get("narration",""));duration=max(2.0,min(22.0,len(narration.split())/2.35+1.2))
        beat=dict(b);beat["id"]=beat.get("id",f"beat-{i+1}");beat["start"]=round(cursor,3);beat["end"]=round(cursor+duration,3);beat["assets"]=assets_by_beat[i] if i<len(assets_by_beat) else [];beat["actions"]=beat.get("actions",[]);beat["sfx"]=beat.get("sfx",[]);beat=build_shots(beat);beats.append(beat);cursor+=duration
    m={"version":2,"title":plan.get("title",plan["topic"]),"topic":plan["topic"],"duration":round(cursor,3),"fps":profile["fps"],"width":profile["width"],"height":profile["height"],"audioSrc":audio_src,"beats":beats,"captions":words,"sources":plan.get("sources",[])}
    Path(out).write_text(json.dumps(m,indent=2),encoding="utf-8");return out