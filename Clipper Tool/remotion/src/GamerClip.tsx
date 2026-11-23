import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export interface SubtitleItem {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface GamerClipProps {
  hookText: string;
  facecamSource?: string;
  gameplaySource?: string;
  subtitles?: SubtitleItem[];
}

export const GamerClipTemplate: React.FC<GamerClipProps> = ({
  hookText = "ONE STARE, AND SHE'S GONE",
  facecamSource,
  gameplaySource,
  subtitles = [
    { text: "ONE", startFrame: 10, endFrame: 40 },
    { text: "STARE", startFrame: 40, endFrame: 80 },
    { text: "AND", startFrame: 80, endFrame: 110 },
    { text: "SHE'S", startFrame: 110, endFrame: 150 },
    { text: "GONE", startFrame: 150, endFrame: 200 },
    { text: "real", startFrame: 200, endFrame: 280 },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const faceImg = facecamSource || staticFile("gamer_face.jpg");
  const gameImg = gameplaySource || staticFile("gameplay.jpg");

  // Entrance spring animation for the hook badge
  const hookScale = spring({
    frame,
    fps,
    config: {
      damping: 14,
      stiffness: 140,
    },
  });

  // Find active subtitle
  const currentSubtitle = subtitles.find(
    (s) => frame >= s.startFrame && frame <= s.endFrame
  );

  // Dynamic spring pop animation for each 2-3 word subtitle entry
  const subFrame = currentSubtitle ? frame - currentSubtitle.startFrame : 0;
  const subScale = currentSubtitle
    ? spring({
        frame: subFrame,
        fps,
        config: {
          damping: 12,
          stiffness: 240,
          mass: 0.4,
        },
      })
    : 1;

  const isFaceVideo = Boolean(faceImg && faceImg.includes(".mp4"));
  const isGameVideo = Boolean(gameImg && gameImg.includes(".mp4"));

  return (
    <>
      <AbsoluteFill
        style={{
          backgroundColor: "#000000",
          fontFamily: "'Inter', 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif",
        }}
      >
        {/* 1. TOP 30% SCREEN: GAMER FACE / CAM (100% WIDTH) */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "30%",
            overflow: "hidden",
            backgroundColor: "#111116",
          }}
        >
          {isFaceVideo ? (
            <Video
              src={faceImg}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "center center",
              }}
            />
          ) : (
            <Img
              src={faceImg}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "center 20%",
              }}
            />
          )}
        </div>
      
        {/* 2. BETWEEN FACE & GAMEPLAY: CATCHY VIRAL HOOK BADGE (3-4 WORDS) */}
        <div
          style={{
            position: "absolute",
            top: "26.5%",
            left: "50%",
            transform: `translateX(-50%) scale(${hookScale})`,
            zIndex: 60,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            pointerEvents: "none",
            width: "max-content",
            maxWidth: "94%",
          }}
        >
          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: 20,
              padding: "22px 52px",
              boxShadow:
                "0 14px 40px rgba(0, 0, 0, 0.7), 0 4px 14px rgba(0, 0, 0, 0.4)",
              border: "1px solid rgba(255, 255, 255, 0.9)",
              textAlign: "center",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <span
              style={{
                color: "#050505",
                fontSize: 48,
                fontWeight: 900,
                letterSpacing: "-0.5px",
                lineHeight: 1,
                textTransform: "uppercase",
                whiteSpace: "nowrap",
                display: "inline-block",
              }}
            >
              {hookText}
            </span>
          </div>
        </div>
      
        {/* 3. BOTTOM 70% SCREEN: GAMEPLAY AREA (100% WIDTH) */}
        <div
          style={{
            position: "absolute",
            top: "30%",
            left: 0,
            width: "100%",
            height: "70%",
            overflow: "hidden",
            backgroundColor: "#0d0f12",
          }}
        >
          {isGameVideo ? (
            <Video
              src={gameImg}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "center center",
              }}
            />
          ) : (
            <Img
              src={gameImg}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "center top",
              }}
            />
          )}
      
          {/* 4. DYNAMIC BOTTOM SUBTITLE (CENTERED, SINGLE LINE, NO BACKGROUND BOX, WORD POP) */}
          {currentSubtitle && (
            <div
              style={{
                position: "absolute",
                bottom: 140,
                left: 0,
                right: 0,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                textAlign: "center",
                zIndex: 40,
                pointerEvents: "none",
              }}
            >
              <span
                style={{
                  color: "#FFFFFF",
                  fontSize: 44,
                  fontWeight: 900,
                  letterSpacing: "0.5px",
                  whiteSpace: "nowrap",
                  textAlign: "center",
                  display: "inline-block",
                  transform: `scale(${subScale})`,
                  textShadow:
                    "0 4px 14px rgba(0,0,0,0.95), -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 0 10px rgba(0,0,0,0.8)",
                }}
              >
                {currentSubtitle.text}
              </span>
            </div>
          )}
        </div>
      </AbsoluteFill>
    </>
  );
};
