import React from "react";
import {Composition} from "remotion";
import {JackPocketsVideo} from "./JackPocketsVideo";
import type {VideoManifest} from "./types";

const demo:VideoManifest={
  title:"AutoVideo Demo",topic:"Demo",duration:30,fps:30,width:1920,height:1080,audioSrc:"",
  captions:[],
  beats:[{id:"demo",kind:"cold-open",narration:"A story can start with one strange detail.",start:0,end:30,
    intensity:.85,keywords:["story"],assets:[],overlays:[{type:"headline",text:"ONE STRANGE DETAIL"}]}]
};

export const Root:React.FC=()=>(
  <Composition id="JackPocketsVideo" component={JackPocketsVideo}
    durationInFrames={demo.duration*demo.fps} fps={demo.fps} width={demo.width} height={demo.height}
    defaultProps={{manifest:demo}}/>
);
