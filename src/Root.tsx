import React from "react";
import {Composition} from "remotion";
import {JackPocketsVideo} from "./JackPocketsVideo";
import type {VideoManifest} from "./types";

const demo:VideoManifest={title:"AutoVideo",topic:"Demo",duration:20,fps:30,width:1920,height:1080,audioSrc:"",captions:[],beats:[
{id:"b1",kind:"cold-open",narration:"This is where the story begins.",start:0,end:20,intensity:.9,keywords:["story"],assets:[],overlays:[{type:"headline",text:"THIS IS WHERE IT BEGINS"}],actions:[{type:"zoom",at:0,duration:20,intensity:.25}],sfx:[]}
]};
export const Root:React.FC=()=> <Composition id="JackPocketsVideo" component={JackPocketsVideo} durationInFrames={demo.duration*demo.fps} fps={demo.fps} width={demo.width} height={demo.height} defaultProps={{manifest:demo}}/>;