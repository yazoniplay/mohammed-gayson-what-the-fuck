import React from "react";
import {AbsoluteFill,Audio,Img,interpolate,useCurrentFrame,useVideoConfig} from "remotion";
import type {VideoManifest,Beat} from "./types";
const BeatLayer:React.FC<{beat:Beat;frame:number;fps:number}>=({beat,frame,fps})=>{
 const t=frame/fps-beat.start; const opacity=interpolate(t,[0,.3],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 const scale=interpolate(t,[0,.7],[1.08,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
 return <AbsoluteFill style={{opacity,transform:`scale(${scale})`}}>
  {beat.assets[0]?.src?<Img src={beat.assets[0].src} style={{width:"100%",height:"100%",objectFit:"cover"}}/>:<AbsoluteFill style={{background:"#111"}}/>}
  <AbsoluteFill style={{background:"linear-gradient(90deg,rgba(0,0,0,.86),rgba(0,0,0,.15) 70%,rgba(0,0,0,.55))"}}/>
  <div style={{position:"absolute",left:90,bottom:120,maxWidth:1250,fontFamily:"Arial Black",fontSize:76,lineHeight:1.02,textTransform:"uppercase",color:"#fff"}}>{beat.overlays[0]?.text}</div>
  <div style={{position:"absolute",right:70,top:60,fontFamily:"monospace",fontSize:20,color:"#fff",opacity:.75}}>{beat.kind.toUpperCase()} // {Math.round(beat.intensity*100)}%</div>
 </AbsoluteFill>
};
export const JackPocketsVideo:React.FC<{manifest:VideoManifest}>=({manifest})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const time=frame/fps;
 const beat=manifest.beats.find(b=>time>=b.start&&time<b.end)||manifest.beats.at(-1);
 return <AbsoluteFill style={{background:"#111"}}>{beat&&<BeatLayer beat={beat} frame={frame} fps={fps}/>}
 {manifest.audioSrc&&<Audio src={manifest.audioSrc}/>}
 <div style={{position:"absolute",left:0,right:0,bottom:36,height:4,background:"rgba(255,255,255,.2)"}}>
 <div style={{height:"100%",width:`${Math.min(100,time/manifest.duration*100)}%`,background:"#fff"}}/></div></AbsoluteFill>;
};