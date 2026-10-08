from __future__ import annotations
import os, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def synthesize(text:str,out:Path)->Path:
    key=os.getenv("ELEVENLABS_API_KEY")
    voice=os.getenv("ELEVENLABS_VOICE_ID")
    if not key or not voice: raise RuntimeError("ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID are required for real narration")
    url=f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    r=requests.post(url,headers={"xi-api-key":key,"accept":"audio/mpeg","content-type":"application/json"},
      json={"text":text,"model_id":os.getenv("ELEVENLABS_MODEL","eleven_multilingual_v2"),
            "voice_settings":{"stability":.45,"similarity_boost":.8,"style":.2,"use_speaker_boost":True}},timeout=120)
    r.raise_for_status(); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(r.content); return out
