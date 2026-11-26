import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  staticFile,
  useCurrentFrame,
} from "remotion";

export interface SubtitleItem {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface GamerOverlayProps {
  facecamSource?: string;
  gameplaySource?: string;
  subtitles?: SubtitleItem[];
}

export const GamerOverlayTemplate: React.FC<GamerOverlayProps> = ({
  facecamSource,
  gameplaySource,
  subtitles = [
    { text: "LOOK AT THIS", startFrame: 10, endFrame: 60 },
    { text: "CLUTCH MOMENT", startFrame: 60, endFrame: 120 },
    { text: "RIGHT NOW", startFrame: 120, endFrame: 180 },
    { text: "UNBELIEVABLE GAMEPLAY", startFrame: 180, endFrame: 240 },
    { text: "LET'S GO", startFrame: 240, endFrame: 300 },
  ],
}) => {
  const frame = useCurrentFrame();

  const faceImg = facecamSource || staticFile("gamer_face.jpg");
  const gameImg = gameplaySource || staticFile("gameplay.jpg");

  const isFaceVideo = Boolean(faceImg && faceImg.includes(".mp4"));
  const isGameVideo = Boolean(gameImg && gameImg.includes(".mp4"));

  // Find active subtitle group
  const currentSubtitle = subtitles.find(
    (s) => frame >= s.startFrame && frame <= s.endFrame
  );

  // Split into words for word-by-word reveal (NO pop animation)
  const words = currentSubtitle ? currentSubtitle.text.trim().split(/\s+/) : [];
  const subDuration = currentSubtitle
    ? Math.max(1, currentSubtitle.endFrame - currentSubtitle.startFrame)
    : 1;
  const subProgress = currentSubtitle
    ? Math.max(0, Math.min(0.999, (frame - currentSubtitle.startFrame) / subDuration))
    : 0;
  const activeWordIndex = Math.min(
    words.length - 1,
    Math.floor(subProgress * words.length)
  );

  return (
    <>
      <AbsoluteFill
        style={{
          backgroundColor: "#000000",
          fontFamily:
            "'Montserrat', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
        }}
      >
        {/* ============================================================== */}
        {/* 1. TOP 15% EMPTY SPACE (PERMANENTLY CLEAN & EMPTY)             */}
        {/* ============================================================== */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "15%",
            backgroundColor: "#000000",
            zIndex: 10,
          }}
        />
      
        {/* ============================================================== */}
        {/* 2. MIDDLE 70% GAMEPLAY AREA (Height: 70% = 1344px)              */}
        {/* ============================================================== */}
        <div
          style={{
            position: "absolute",
            top: "15%",
            left: 0,
            width: "100%",
            height: "70%",
            overflow: "hidden",
            backgroundColor: "#0d0f12",
          }}
        >
          {/* Full Gameplay Layer */}
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
                objectPosition: "center center",
              }}
            />
          )}
      
          {/* Small Gamer Face Cam - Right Corner PIP Overlay */}
          <div
            style={{
              position: "absolute",
              top: 14,
              right: 20,
              width: 400,
              height: 250,
              borderRadius: 20,
              overflow: "hidden",
              border: "3.5px solid #FFFFFF",
              boxShadow: "0 10px 28px rgba(0, 0, 0, 0.6)",
              backgroundColor: "#16161a",
              zIndex: 40,
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
      
          {/* Word-by-Word Caption Overlay (Bottom-Middle of Gameplay, No Pop Animation) */}
          {currentSubtitle && words.length > 0 && (
            <div
              style={{
                position: "absolute",
                bottom: 48,
                left: 0,
                right: 0,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 50,
                pointerEvents: "none",
                paddingLeft: 40,
                paddingRight: 40,
              }}
            >
              <div
                style={{
                  display: "inline-flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: "12px 18px",
                  padding: "8px 16px",
                  maxWidth: "94%",
                }}
              >
                {words.map((word, idx) => {
                  const isVisible = idx <= activeWordIndex;
                  const isActive = idx === activeWordIndex;

                  if (!isVisible) return null; // Reveals word-by-word

                  return (
                    <span
                      key={idx}
                      style={{
                        color: isActive ? "#FFE600" : "#FFFFFF",
                        fontSize: 52,
                        fontWeight: 900,
                        letterSpacing: "0.5px",
                        textTransform: "uppercase",
                        lineHeight: 1.1,
                        textShadow: "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000",
                      }}
                    >
                      {word}
                    </span>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      
        {/* ============================================================== */}
        {/* 3. BOTTOM 15% EMPTY SPACE (Height: 15% = 288px)                 */}
        {/* ============================================================== */}
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            width: "100%",
            height: "15%",
            backgroundColor: "#000000",
            zIndex: 10,
          }}
        />
      </AbsoluteFill>
    </>
  );
};
