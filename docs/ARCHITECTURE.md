# MixaClip Architecture & Pipeline Overview

## 1. High-Level Architecture

MixaClip is built with a pure Python + native FFmpeg C++ compositing engine.

```
Long Stream (16:9 MP4) ──► faster-whisper (INT8 CPU) ──► Verbatim Subtitles (Roman Hinglish)
           │
           ├──► PySceneDetect (Scene Detection) ──► Moment Scoring (28s Windows)
           │
           ▼
User Approval Gate ──► Native FFmpeg + ASS Burn-in Engine
           │
           ▼
9:16 Vertical Short (Output/Project_X/clip_0X.mp4)
- Top 30%: Proportional Facecam
- Center: High-Contrast Viral Hook Badge Pill
- Bottom 70%: Proportional Real Gameplay (Zero Distortion)
- Lower Third: 2-3 Word Pop Hinglish Subtitles
```

## 2. No-Stretch Aspect Ratio Standard

All video transformations strictly enforce:
```
scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1
```
This guarantees that gameplay footage and gamer webcam frames fill their allocated vertical canvas without stretching, compressing, or skewing pixel geometry.
