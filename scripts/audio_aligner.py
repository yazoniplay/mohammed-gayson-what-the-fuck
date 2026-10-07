from pathlib import Path
import json
def align(audio_path:str,out_path:str,model_name:str="small")->Path:
 from faster_whisper import WhisperModel
 model=WhisperModel(model_name,compute_type="int8")
 segments,_=model.transcribe(audio_path,word_timestamps=True)
 words=[{"word":w.word,"start":w.start,"end":w.end} for s in segments for w in (s.words or [])]
 out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(words,indent=2),encoding="utf-8"); return out
if __name__=="__main__":
 import argparse
 p=argparse.ArgumentParser(); p.add_argument("audio"); p.add_argument("--out",default="data/runs/alignment.json"); p.add_argument("--model",default="small"); a=p.parse_args(); print(align(a.audio,a.out,a.model))
