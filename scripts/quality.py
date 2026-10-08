from __future__ import annotations
import json
from pathlib import Path

def validate(manifest_path:str)->list[str]:
    m=json.loads(Path(manifest_path).read_text()); errors=[]
    if not m.get("beats"): errors.append("manifest has no beats")
    if m.get("duration",0)<=0: errors.append("duration must be positive")
    last=0
    for b in m["beats"]:
        if b["start"]<last: errors.append(f"overlapping beat: {b['id']}")
        if b["end"]<=b["start"]: errors.append(f"invalid timing: {b['id']}")
        last=b["end"]
    return errors
