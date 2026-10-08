import type {RenderProfile} from "./types";

export const profiles: Record<RenderProfile,{width:number;height:number;fps:number}> = {
  youtube:{width:1920,height:1080,fps:30},
  shorts:{width:1080,height:1920,fps:30},
  square:{width:1080,height:1080,fps:30},
  "4k":{width:3840,height:2160,fps:30}
};

export const palette = { bg:"#0b0b0b", fg:"#f5f2ea", muted:"#aaa69d", accent:"#e8c547" };
