from __future__ import annotations
import json
from pathlib import Path
def validate(path:str)->list[str]:
    m=json.loads(Path(path).read_text());e=[]
    if m.get("version")!=2:e.append("unsupported manifest version")
    if not m.get("beats"):e.append("manifest has no beats")
    if m.get("duration",0)<=0:e.append("duration must be positive")
    last=0
    for b in m["beats"]:
        if b["start"]<last:e.append(f"overlapping beat: {b['id']}")
        if b["end"]<=b["start"]:e.append(f"invalid beat timing: {b['id']}")
        for s in b.get("shots",[]):
            if s["end"]<=s["start"]:e.append(f"invalid shot timing: {s['id']}")
            if s["start"]<0 or s["end"]>b["end"]-b["start"]+.05:e.append(f"shot outside beat: {s['id']}")
        last=b["end"]
    return e