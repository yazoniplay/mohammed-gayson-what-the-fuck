import React from "react";
import {AbsoluteFill,Audio,Img,interpolate,useCurrentFrame,useVideoConfig,Sequence,staticFile} from "remotion";
import type {VideoManifest,Beat,Shot,Layer} from "./types";
const src=(s:string)=>s.startsWith("http")?s:staticFile(s);
const shadow="0 4px 24px rgba(0,0,0,.85)";
const ease=(x:number)=>x*x*(3-2*x);
const clamp=(x:number,a=0,b=1)=>Math.max(a,Math.min(b,x));
const LayerView:React.FC<{layer:Layer;beat:Beat;shot:Shot;frame:number;fps:number}>=({layer,beat,shot,frame,fps})=>{
 const t=Math.max(0,frame/fps-(beat.start+shot.start)),d=Math.max(.01,shot.end-shot.start);
 const p=interpolate(t,[0,Math.min(.22,d)],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const sc=layer.animation==="push"?interpolate(t,[0,d],[1.10,1],{extrapolateRight:"clamp"}):layer.animation==="pull"?interpolate(t,[0,d],[1,1.10],{extrapolateRight:"clamp"}):1;
 const panX=layer.animation==="pan"?interpolate(t,[0,d],[-3,3],{extrapolateRight:"clamp"}):0;
 const panY=layer.animation==="parallax"?interpolate(t,[0,d],[2,-2],{extrapolateRight:"clamp"}):0;
 const base:React.CSSProperties={position:"absolute",left:`${layer.x}%`,top:`${layer.y}%`,width:`${layer.width}%`,height:`${layer.height}%`,opacity:layer.opacity*p,zIndex:layer.z,transform:`translate(${panX}%,${panY}%) rotate(${layer.rotation}deg) scale(${sc})`};
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
 const zoom=shot.actions.find(a=>a.type==="zoom"),blur=shot.actions.find(a=>a.type==="blur"),glitch=shot.actions.find(a=>a.type==="glitch"),whip=shot.actions.find(a=>a.type==="whip");
 const zoomScale=zoom?1+zoom.intensity*.16*clamp(local/Math.max(.01,zoom.duration)):1;
 const blurPx=blur?blur.intensity*5:0;
 const glitchX=glitch?Math.sin(local*170)*glitch.intensity*7:0;
 const whipX=whip?interpolate(local,[Math.max(0,whip.at*d-.10),Math.max(.01,whip.at*d)],[0,whip.intensity*90],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}):0;
 const fp=flash?interpolate(local,[flash.at*d,flash.at*d+flash.duration],[.4,0],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}):0;
 const dx=shake?Math.sin(local*80)*shake.intensity*10:0;
 return <AbsoluteFill style={{overflow:"hidden",background:"#080808",transform:`translate(${dx+glitchX+whipX}px,0) scale(${zoomScale})`,filter:`blur(${blurPx}px)`}}>
  {shot.layers.map(l=><LayerView key={l.id} layer={l} beat={beat} shot={shot} frame={frame} fps={fps}/>)}
  {fp>0&&<AbsoluteFill style={{background:"#fff",opacity:fp,zIndex:30}}/>}
  {glitch&&<AbsoluteFill style={{opacity:.10,mixBlendMode:"screen",transform:`translateX(${-glitchX}px)`,background:"linear-gradient(transparent 46%,rgba(255,255,255,.8) 47%,transparent 49%,transparent 52%,rgba(255,255,255,.35) 53%,transparent 55%)",zIndex:31}}/>}
  <AbsoluteFill style={{pointerEvents:"none",boxShadow:"inset 0 0 180px rgba(0,0,0,.72)",zIndex:32}}/>
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