export type BeatKind="cold-open"|"context"|"escalation"|"reveal"|"fallout"|"ending";
export type RenderProfile="youtube"|"shorts"|"square"|"4k";
export type VisualAsset={id:string;kind:"photo"|"video"|"generated"|"document"|"texture";src:string;credit?:string;license?:string;score:number};
export type Beat={id:string;kind:BeatKind;narration:string;start:number;end:number;intensity:number;keywords:string[];assets:VisualAsset[];overlays:Array<{type:"headline"|"label"|"stat"|"stamp"|"quote";text:string}>};
export type VideoManifest={title:string;topic:string;duration:number;fps:number;width:number;height:number;audioSrc:string;beats:Beat[];captions:Array<{word:string;start:number;end:number}>};
