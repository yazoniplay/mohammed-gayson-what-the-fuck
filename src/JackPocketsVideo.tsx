import React from "react";
import {AbsoluteFill,Audio,Img,interpolate,useCurrentFrame,useVideoConfig,Sequence,staticFile} from "remotion";
import type {VideoManifest,Beat} from "./types";

const Visual:React.FC<{beat:Beat;frame:number;fps:number}>=({beat,frame,fps})=>{
  const t=frame/fps-beat.start;
  const enter=interpolate(t,[0,.25],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const zoom=interpolate(t,[0,beat.end-beat.start],[1.07,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const asset=beat.assets.find(a=>a.kind==="photo"||a.kind==="generated"||a.kind==="document");
  return <AbsoluteFill style={{opacity:enter,transform:`scale(${zoom})`,overflow:"hidden"}}>
    {asset?<Img src={asset.src.startsWith("http")?asset.src:staticFile(asset.src)} style={{width:"100%",height:"100%",objectFit:"cover"}}/>:<AbsoluteFill style={{background:"#111"}}/>}
    <AbsoluteFill style={{background:"linear-gradient(90deg,rgba(0,0,0,.9),rgba(0,0,0,.15) 70%,rgba(0,0,0,.6))"}}/>
    <div style={{position:"absolute",left:75,bottom:110,maxWidth:"68%",fontFamily:"Arial Black,Arial",fontSize:78,lineHeight:.98,textTransform:"uppercase",color:"#fff",letterSpacing:-2}}>
      {beat.overlays[0]?.text}
    </div>
    <div style={{position:"absolute",right:55,top:45,fontFamily:"monospace",fontSize:18,color:"#fff",opacity:.65}}>
      {beat.kind.toUpperCase()} // {Math.round(beat.intensity*100)}%
    </div>
  </AbsoluteFill>
};

export const JackPocketsVideo:React.FC<{manifest:VideoManifest}>=({manifest})=>{
  const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const time=frame/fps;
  return <AbsoluteFill style={{background:"#111",fontFamily:"Arial"}}>
    {manifest.beats.map((beat)=>(
      <Sequence key={beat.id} from={Math.round(beat.start*fps)} durationInFrames={Math.max(1,Math.round((beat.end-beat.start)*fps))}>
        <Visual beat={beat} frame={frame} fps={fps}/>
      </Sequence>
    ))}
    {manifest.audioSrc&&<Audio src={staticFile(manifest.audioSrc)} volume={1}/>}
    {manifest.captions.length>0&&<div style={{position:"absolute",left:"10%",right:"10%",bottom:45,textAlign:"center",fontSize:30,fontWeight:700,color:"#fff",textShadow:"0 2px 8px #000"}}>
      {manifest.captions.find(w=>time>=w.start&&time<w.end)?.word||""}
    </div>}
    <div style={{position:"absolute",left:0,right:0,bottom:0,height:5,background:"rgba(255,255,255,.18)"}}>
      <div style={{height:"100%",width:`${Math.min(100,time/manifest.duration*100)}%`,background:"#fff"}}/>
    </div>
  </AbsoluteFill>;
};
