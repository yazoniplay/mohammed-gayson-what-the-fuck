import React from "react";
import {AbsoluteFill,Audio,Img,interpolate,useCurrentFrame,useVideoConfig,Sequence,staticFile} from "remotion";
import type {VideoManifest,Beat,Shot,Layer} from "./types";
const src=(s:string)=>s.startsWith("http")?s:staticFile(s);
const shadow="0 4px 24px rgba(0,0,0,.85)";
const LayerView:React.FC<{layer:Layer;beat:Beat;shot:Shot;frame:number;fps:number}>=({layer,beat,shot,frame,fps})=>{
 const t=Math.max(0,frame/fps-(beat.start+shot.start)),d=Math.max(.01,shot.end-shot.start);
 const p=interpolate(t,[0,Math.min(.22,d)],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const sc=layer.animation==="push"?interpolate(t,[0,d],[1.07,1],{extrapolateRight:"clamp"}):layer.animation==="pull"?interpolate(t,[0,d],[1,1.07],{extrapolateRight:"clamp"}):1;
 const base:React.CSSProperties={position:"absolute",left:`${layer.x}%`,top:`${layer.y}%`,width:`${layer.width}%`,height:`${layer.height}%`,opacity:layer.opacity*p,zIndex:layer.z,transform:`rotate(${layer.rotation}deg) scale(${sc})`};
 if(layer.kind==="image"&&layer.assetId){const a=beat.assets.find(x=>x.id===layer.assetId);return a?<Img src={src(a.src)} style={{...base,objectFit:"cover"}}/>:null}
 if(layer.kind==="highlight")return <div style={{...base,background:"rgba(245,205,40,.38)",mixBlendMode:"screen"}}/>;
 if(layer.kind==="arrow")return <div style={{...base,color:"#fff",fontSize:"4vw",fontWeight:900,textShadow}}>{layer.text||"→"}</div>;
 if(layer.kind==="label")return <div style={{...base,boxSizing:"border-box",background:"rgba(0,0,0,.68)",border:"1px solid rgba(255,255,255,.45)",padding:"6px 10px",fontFamily:"monospace",fontWeight:800,fontSize:"1.2vw",letterSpacing:2,color:"#fff"}}>{layer.text}</div>;
 if(layer.kind==="text")return <div style={{...base,fontFamily:"Arial Black,Arial",fontWeight:900,fontSize:"clamp(34px,5vw,96px)",lineHeight:.9,letterSpacing:-3,color:"#f5f2ea",textTransform:"uppercase",textShadow}}>{layer.text}</div>;
 return null;
};
const ShotView:React.FC<{beat:Beat;shot:Shot;frame:number;fps:number}>=({beat,shot,frame,fps})=>{
 const local=frame/fps-(beat.start+shot.start),d=shot.end-shot.start;
 const flash=shot.actions.find(a=>a.type==="flash"),shake=shot.actions.find(a=>a.type==="shake");
 const fp=flash?interpolate(local,[flash.at*d,flash.at*d+flash.duration],[.4,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}):0;
 const dx=shake?Math.sin(local*80)*shake.intensity*10:0;
 return <AbsoluteFill style={{overflow:"hidden",background:"#080808",transform:`translateX(${dx}px)`}}>
  {shot.layers.map(l=><LayerView key={l.id} layer={l} beat={beat} shot={shot} frame={frame} fps={fps}/>)}
  {fp>0&&<AbsoluteFill style={{background:"#fff",opacity:fp,zIndex:30}}/>}
 </AbsoluteFill>;
};
const cap=(w:any[],t:number)=>w.find((x:any)=>t>=x.start&&t<x.end)?.word||"";
export const JackPocketsVideo:React.FC<{manifest:VideoManifest}>=({manifest})=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig(),time=frame/fps;
 return <AbsoluteFill style={{background:"#080808"}}>
  {manifest.beats.flatMap(b=>b.shots.map(s=><Sequence key={s.id} from={Math.round((b.start+s.start)*fps)} durationInFrames={Math.max(1,Math.round((s.end-s.start)*fps))}><ShotView beat={b} shot={s} frame={frame} fps={fps}/></Sequence>))}
  {manifest.audioSrc&&<Audio src={staticFile(manifest.audioSrc)}/>}
  {manifest.musicSrc&&<Audio src={staticFile(manifest.musicSrc)} volume={.11}/>}
  <div style={{position:"absolute",left:"8%",right:"8%",bottom:"4%",height:48,display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"Arial Black,Arial",fontSize:"clamp(20px,2.1vw,40px)",color:"#fff",textShadow}}>{cap(manifest.captions,time)}</div>
  <div style={{position:"absolute",left:0,right:0,bottom:0,height:4,background:"rgba(255,255,255,.14)",zIndex:100}}><div style={{height:"100%",width:`${Math.min(100,time/manifest.duration*100)}%`,background:"#fff"}}/></div>
 </AbsoluteFill>;
};