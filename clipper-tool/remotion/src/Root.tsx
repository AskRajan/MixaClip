import React from "react";
import { Composition, staticFile } from "remotion";
import { GamerClipTemplate } from "./GamerClip";
import { GamerOverlayTemplate } from "./GamerOverlayTemplate";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ============================================================== */}
      {/* TEMPLATE 1: SPLIT SCREEN (Top 30% Facecam + Hook + Bottom 70% Game) */}
      {/* ============================================================== */}
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

      {/* ============================================================== */}
      {/* TEMPLATE 2: CORNER PIP OVERLAY (15% Empty Top/Bottom + PIP Face) */}
      {/* ============================================================== */}
      <Composition
        id="GamerOverlayDemo"
        component={GamerOverlayTemplate}
        durationInFrames={300}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{
          facecamSource: staticFile("gamer_face.jpg"),
          gameplaySource: staticFile("gameplay.jpg"),
        }}
      />
    </>
  );
};
