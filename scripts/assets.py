from __future__ import annotations
import os, requests, re
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def search_pexels(query:str,out:Path,limit:int=3)->list[dict]:
    key=os.getenv("PEXELS_API_KEY")
    if not key: return []
    r=requests.get("https://api.pexels.com/v1/search",headers={"Authorization":key},params={"query":query,"per_page":limit,"orientation":"landscape"},timeout=30)
    r.raise_for_status()
    result=[]
    for i,p in enumerate(r.json().get("photos",[])):
        src=p.get("src",{}).get("large2x") or p.get("src",{}).get("large")
        if not src: continue
        path=out/f"asset-{len(result)}.jpg"
        data=requests.get(src,timeout=60); data.raise_for_status(); path.write_bytes(data.content)
        result.append({"id":str(p["id"]),"kind":"photo","src":str(path),"credit":p.get("photographer"),"license":"Pexels","score":1})
    return result
