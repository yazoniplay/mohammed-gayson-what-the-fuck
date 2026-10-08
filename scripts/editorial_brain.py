from __future__ import annotations
import re,random
STOP={"the","a","an","and","or","but","of","to","in","on","for","with","is","was","are","were","this","that","it","as","at","by","from","into","about","then","than"}
def sentences(text:str)->list[str]: return [x.strip() for x in re.split(r"(?<=[.!?])\s+",text.strip()) if x.strip()]
def classify(s:str):
    low=s.lower()
    if any(x in low for x in ["but","however","except","instead","yet"]): return "contrast","evidence",.86
    if any(x in low for x in ["because","means","caused","after","before","according"]): return "explain","evidence",.68
    if any(x in low for x in ["suddenly","revealed","secret","actually","truth","discovered"]): return "reveal","reveal",.95
    if any(x in low for x in ["died","collapsed","lost","failed","ended","disappeared"]): return "consequence","consequence",.90
    if "?" in s:return "punchline","punchline",.90
    return "setup","setup",.52
def keywords(s:str)->list[str]:
    words=re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]{2,}",s)
    return list(dict.fromkeys(w.lower() for w in words if w.lower() not in STOP))[:6]
def _span(sentence,words,pos):
    target=re.findall(r"[a-z0-9]+",sentence.lower()); flat=[re.findall(r"[a-z0-9]+",str(w.get("word","")).lower()) for w in words]
    flat=[x[0] for x in flat if x]
    for i in range(pos,len(flat)):
        if flat[i:i+len(target)]==target:return i,i+len(target)
    return pos,min(len(words),pos+max(1,len(target)))
def build_shots(beat,seed=42,aligned_words=None,sentences_override=None):
    random.seed(seed+sum(ord(c) for c in beat.get("id",""))); ss=sentences_override or sentences(str(beat.get("narration",""))) or [str(beat.get("narration",""))]
    total=max(.2,float(beat["end"])-float(beat["start"]));assets=beat.get("assets",[]);shots=[];pos=0
    for i,s in enumerate(ss):
        intent,reason,intensity=classify(s)
        if aligned_words:
            a,z=_span(s,aligned_words,pos);pos=z
            start=max(0,float(aligned_words[a]["start"])-float(beat["start"])) if a<len(aligned_words) else 0
            end=min(total,float(aligned_words[z-1]["end"])-float(beat["start"])) if z>a else start+.5
        else:
            start=sum(x["end"]-x["start"] for x in shots);end=start+max(.45,total/max(1,len(ss)))
        end=max(start+.25,end)
        if i==len(ss)-1:end=total
        aids=[a.get("id") for a in assets[:1] if a.get("id")];kw=keywords(s);layers=[]
        if aids:layers.append({"id":f"img-{i}","kind":"image","assetId":aids[0],"x":0,"y":0,"width":100,"height":100,"rotation":0,"opacity":1,"z":0,"animation":"push" if intensity>.6 else "pan"})
        if kw:layers.append({"id":f"kw-{i}","kind":"text","text":kw[0].upper(),"x":7,"y":70,"width":65,"height":18,"rotation":0,"opacity":.98,"z":5,"animation":"static"})
        if reason in ("evidence","reveal"):layers.append({"id":f"label-{i}","kind":"label","text":reason.upper(),"x":7,"y":7,"width":22,"height":5,"rotation":0,"opacity":.85,"z":6,"animation":"static"})
        if intensity>.82:layers.append({"id":f"hl-{i}","kind":"highlight","text":kw[0].upper() if kw else "KEY DETAIL","x":7,"y":61,"width":38,"height":8,"rotation":-2,"opacity":.75,"z":4,"animation":"freeze"})
        acts=[{"type":"cut","at":0,"duration":.05,"intensity":intensity,"reason":reason},{"type":"zoom" if intensity>.65 else "pan","at":.12,"duration":min(.8,max(.2,(end-start)*.5)),"intensity":min(1,intensity*.65),"reason":"pace"}]
        if reason=="reveal":acts += [{"type":"flash","at":.82,"duration":.09,"intensity":.45,"reason":"reveal"},{"type":"glitch","at":.84,"duration":.12,"intensity":.18,"reason":"reveal"}]
        if intensity>.88:acts.append({"type":"shake","at":.84,"duration":.16,"intensity":.25,"reason":"emphasis"})
        shots.append({"id":f"{beat['id']}-shot-{i}","start":round(start,3),"end":round(end,3),"reason":reason,"intent":intent,"assetIds":aids,"layers":layers,"actions":acts,"sfx":[],"intensity":round(intensity,2)})
    beat["shots"]=shots;return beat