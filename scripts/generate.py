from __future__ import annotations
import argparse,json,re,subprocess
from pathlib import Path
from llm import generate
from tts import synthesize
from assets import search_pexels
from research import search_web
from manifest import build
from quality import validate
PROFILES={"youtube":{"width":1920,"height":1080,"fps":60}}
def slug(s:str)->str:return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:55] or "run"
def main():
 p=argparse.ArgumentParser(description="Generate an editorially planned documentary video.")
 p.add_argument("--topic",required=True);p.add_argument("--profile",choices=PROFILES,default="youtube");p.add_argument("--no-render",action="store_true");p.add_argument("--assets-per-beat",type=int,default=2);a=p.parse_args()
 root=Path("public/runs")/slug(a.topic);root.mkdir(parents=True,exist_ok=True)
 plan=generate(a.topic);plan["topic"]=a.topic
 research=[]
 for b in plan.get("beats",[]):
  q=f"{a.topic}: {b.get('title','')} {b.get('narration','')[:500]}"
  research.extend(search_web(q,limit=3))
 plan["sources"]=list(dict.fromkeys(x["url"] for x in research if x.get("url")))
 (root/"research.json").write_text(json.dumps(research,indent=2),encoding="utf-8")
 (root/"plan.json").write_text(json.dumps(plan,indent=2),encoding="utf-8")
 narration=" ".join(str(b.get("narration","")) for b in plan.get("beats",[]));audio=root/"narration.mp3";synthesize(narration,audio)
 subprocess.run(["python","scripts/audio_aligner.py",str(audio),"--out",str(root/"alignment.json")],check=True)
 words=json.loads((root/"alignment.json").read_text());asset_sets=[]
 for i,b in enumerate(plan.get("beats",[])):
  aset=[]
  for q in list(dict.fromkeys((b.get("keywords") or [a.topic]) + [str(b.get("narration",""))[:120]]))[:a.assets_per_beat]:
   for item in search_pexels(str(q),root/f"assets-{i}",limit=1):
    item["src"]=str(Path(item["src"]).relative_to("public")).replace("\\","/");aset.append(item)
  asset_sets.append(aset)
 manifest=build(plan,str(audio.relative_to("public")).replace("\\","/"),words,asset_sets,PROFILES[a.profile],root/"manifest.json")
 errors=validate(str(manifest))
 if errors:raise SystemExit("QUALITY GATE FAILED:\n"+"\n".join(errors))
 print(f"READY: {manifest}")
 if not a.no_render:subprocess.run(["npx","remotion","render","src/index.tsx","JackPocketsVideo",f"out/{slug(a.topic)}.mp4","--props",str(manifest)],check=True)
if __name__=="__main__":main()