from __future__ import annotations
import os,requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def _download(url,path):
    data=requests.get(url,timeout=60);data.raise_for_status();path.write_bytes(data.content)

def search_pexels(query:str,out:Path,limit:int=3)->list[dict]:
    key=os.getenv("PEXELS_API_KEY")
    if not key:return []
    out.mkdir(parents=True,exist_ok=True)
    r=requests.get("https://api.pexels.com/v1/search",headers={"Authorization":key},params={"query":query,"per_page":max(1,limit),"orientation":"landscape"},timeout=30);r.raise_for_status()
    result=[]
    for p in r.json().get("photos",[]):
        src=p.get("src",{}).get("large2x") or p.get("src",{}).get("large")
        if not src:continue
        path=out/f"photo-{p['id']}.jpg";_download(src,path)
        result.append({"id":str(p["id"]),"kind":"photo","src":str(path),"credit":p.get("photographer"),"license":"Pexels","score":1.0,"role":"b-roll"})
    return result

def make_asset_plan(sentence:str,editorial:dict|None=None)->list[dict]:
    low=sentence.lower();roles=[]
    if any(x in low for x in ["map","country","city","where","location","border"]):roles.append("map")
    if any(x in low for x in ["according","report","document","letter","record","court","file"]):roles.append("document")
    if any(x in low for x in ["percent","million","billion","number","statistic","rate"]):roles.append("chart")
    if any(x in low for x in ["tweet","post","website","message","app","screenshot"]):roles.append("screenshot")
    if not roles:roles=["b-roll","photo"]
    return [{"role":x,"query":sentence[:180]} for x in roles]
