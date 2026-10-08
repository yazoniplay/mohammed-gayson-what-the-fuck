import React from "react";
import {AbsoluteFill,Audio,Img,interpolate,useCurrentFrame,useVideoConfig,Sequence,staticFile} from "remotion";
import type {VideoManifest,Beat,Word} from "./types";

const caption=(words:Word[],t:number)=>words.find(w=>t>=w.start&&t<w.end)?.word||"";
const Visual:React.FC<{beat:Beat;frame:number;fps:number}>=({beat,frame,fps})=>{
 const t=frame/fps-beat.start, len=Math.max(.01,beat.end-beat.start);
 const enter=interpolate(t,[0,.18],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const exit=interpolate(t,[Math.max(0,len-.22),len],[1,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const base=1.035+beat.intensity*.035;
 const zoom=interpolate(t,[0,len],[base,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const asset=beat.assets[0];
 return <AbsoluteFill style={{opacity:enter*exit,transform:`scale(${zoom})`,overflow:"hidden",background:"#0a0a0a"}}>
   {asset?<Img src={asset.src.startsWith("http")?asset.src:staticFile(asset.src)} style={{width:"100%",height:"100%",objectFit:"cover"}}/>:null}
   <AbsoluteFill style={{background:"linear-gradient(90deg,rgba(0,0,0,.88),rgba(0,0,0,.12) 68%,rgba(0,0,0,.58))"}}/>
   <div style={{position:"absolute",left:"5%",bottom:"13%",maxWidth:"70%",fontFamily:"Arial Black,Arial",fontSize:"clamp(54px,4vw,92px)",lineHeight:.93,letterSpacing:-3,textTransform:"uppercase",color:"#f5f2ea",textShadow:"0 5px 25px #000"}}>{beat.overlays[0]?.text}</div>
   <div style={{position:"absolute",left:"5%",top:"7%",fontFamily:"monospace",fontSize:18,color:"#fff",opacity:.7,letterSpacing:2}}>{beat.kind.toUpperCase()} / {String(Math.round(beat.intensity*100)).padStart(3,"0")}</div>
   {beat.overlays.slice(1).map((o,i)=><div key={i} style={{position:"absolute",right:"5%",top:`${16+i*8}%`,padding:"7px 11px",border:"1px solid rgba(255,255,255,.45)",background:"rgba(0,0,0,.45)",fontFamily:"monospace",fontSize:16,color:"#fff"}}>{o.text}</div>)}
 </AbsoluteFill>;
};
export const JackPocketsVideo:React.FC<{manifest:VideoManifest}>=({manifest})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const time=frame/fps;
 return <AbsoluteFill style={{background:"#090909"}}>
 {manifest.beats.map(b=><Sequence key={b.id} from={Math.round(b.start*fps)} durationInFrames={Math.max(1,Math.round((b.end-b.start)*fps))}><Visual beat={b} frame={frame} fps={fps}/></Sequence>)}
 {manifest.audioSrc&&<Audio src={staticFile(manifest.audioSrc)}/>}
 {manifest.musicSrc&&<Audio src={staticFile(manifest.musicSrc)} volume={.12}/>}
 <div style={{position:"absolute",left:"9%",right:"9%",bottom:"4%",height:42,display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"Arial",fontWeight:800,fontSize:30,color:"#fff",textShadow:"0 3px 14px #000"}}>{caption(manifest.captions,time)}</div>
 <div style={{position:"absolute",left:0,right:0,bottom:0,height:4,background:"rgba(255,255,255,.15)"}}><div style={{height:"100%",width:`${Math.min(100,time/manifest.duration*100)}%`,background:"#fff"}}/></div>
 </AbsoluteFill>;
};