from __future__ import annotations
from pathlib import Path
import json, math, shutil

def build(plan:dict,audio:str,words:list[dict],assets_by_beat:list[list[dict]],profile:dict,out:Path)->Path:
    beats=plan.get("beats",[])
    cursor=0.0; built=[]
    for i,b in enumerate(beats):
        narration=str(b.get("narration","")).strip()
        duration=max(4.0,min(22.0,len(narration.split())/2.35+1.2))
        start=cursor; end=start+duration; cursor=end
        ovs=b.get("overlays") or [{"type":"headline","text":b.get("kind","SCENE").upper()}]
        built.append({"id":f"beat-{i+1:02}","kind":b.get("kind","context"),"narration":narration,
          "start":start,"end":end,"intensity":float(b.get("intensity",.6)),
          "keywords":b.get("keywords",[]),"assets":assets_by_beat[i] if i<len(assets_by_beat) else [],"overlays":ovs})
    manifest={"title":plan.get("title","AutoVideo"),"topic":plan.get("topic",""),"duration":cursor,
      "fps":profile["fps"],"width":profile["width"],"height":profile["height"],
      "audioSrc":audio,"beats":built,"captions":words}
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(manifest,indent=2),encoding="utf-8"); return out
