import React from "react";
import { Composition, staticFile } from "remotion";
import { GamerClipTemplate, SubtitleItem } from "./GamerClip";
import clipsData from "./clipsData.json";

interface ClipItem {
  clip_number: number;
  hook_heading: string;
  start_time: string;
  end_time: string;
  start_seconds: number;
  end_seconds: number;
  duration_seconds: number;
  description: string;
  transcript: string;
  chunks_3s: Array<{
    start: number;
    end: number;
    text: string;
  }>;
}

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 5 Real Viral GTA 6 Compositions with Live Video & Audio */}
      {(clipsData as ClipItem[]).map((clip) => {
        const subtitles: SubtitleItem[] = clip.chunks_3s.map((ch) => ({
          text: ch.text,
          startFrame: Math.max(0, Math.round(ch.start * 60)),
          endFrame: Math.round(ch.end * 60),
        }));

        const safeId = `Clip-${clip.clip_number}-${clip.hook_heading.replace(/[^a-zA-Z0-9]+/g, "-")}`;

        return (
          <Composition
            key={clip.clip_number}
            id={safeId}
            component={GamerClipTemplate}
            durationInFrames={Math.round(clip.duration_seconds * 60)}
            fps={60}
            width={1080}
            height={1920}
            defaultProps={{
              hookText: clip.hook_heading,
              facecamSource: staticFile(`clips/clip${clip.clip_number}_face.mp4`),
              gameplaySource: staticFile(`clips/clip${clip.clip_number}_game.mp4`),
              subtitles: subtitles,
            }}
          />
        );
      })}

      {/* Demo Reference Composition */}
      <Composition
        id="GamerClipDemo"
        component={GamerClipTemplate}
        durationInFrames={300}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{
          hookText: "ONE STARE, AND SHE'S GONE",
        }}
      />
    </>
  );
};
