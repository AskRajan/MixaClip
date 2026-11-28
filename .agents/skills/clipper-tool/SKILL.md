---
name: clipper-tool
description: Transcribe gamer MP4 videos, identify best viral moments, present timestamps & hooks for user approval, and ultra-fast export clips via native FFmpeg without browser preview.
---

# Clipper Tool Workflow

Process gamer MP4 videos into high-engagement vertical shorts using `clipper-tool/`.

## Stack
- **Whisper:** `clipper-tool/venv` (`faster-whisper` `small` model, CPU INT8)
- **Scenes:** `PySceneDetect`
- **Video & Compositing:** `clipper-tool/ffmpeg/bin/ffmpeg.exe` (Native ultra-fast pipeline, ~8s per clip)
- **Subtitles & Badges:** Advanced SubStation Alpha (`.ass`) with crisp drop-shadow and bold pill styling.
- **Available Templates:**
  - **Template 1: Split-Screen (`GamerClipTemplate`)** (Top 30% facecam, middle hook badge, bottom 70% gameplay).
  - **Template 2: Corner PIP Overlay (`GamerOverlayTemplate`)** (Top 15% & bottom 15% empty space, full-width gameplay, top-right 400x250px facecam PIP, floating bottom-mid word-by-word captions).
- **Aspect Ratio Rule (STRICT):** Never stretch or squish gameplay video. Always preserve natural aspect ratio using proportional scaling (`force_original_aspect_ratio=increase,crop=...`).

## Output Organization
All exported clips are systematically stored in project subfolders inside `storage/output/`:
- `storage/output/Project_1/*.mp4`
- `storage/output/Project_2/*.mp4`
Each run increments the project folder automatically.

## Procedure (5-Step Execution Workflow)

1. **Step 1: Receive Video URL & Quality Selection (Download Gate):**
   - Input: Video URL provided by the user.
   - Quality: 720p @ 30fps (Recommended for low-end / fast export) or 1080p @ 60fps.
   - Download into `storage/downloads/` via `python -m mixaclip run "<URL>" --quality 720p30`.

2. **Step 2: Language & Template Selection:**
   - Language: Roman Hinglish or English.
   - Template: Split-Screen or Corner PIP.

3. **Step 3: Extract Verbatim Transcript & Identify Viral Moments:**
   - 100% verbatim speech with filler words (*bhai, yaar, arre*), millisecond word alignment, strictly 2-3 words per chunk.
   - High-retention gamer moments (25-30s each) with punchy 3-4 word hook badges.

4. **Step 4: User Approval Gate (Mandatory Permission Step):**
   - Present moments table for user review & confirmation.

5. **Step 5: Ultra-Fast Direct FFmpeg Export:**
   - Run: `python -m mixaclip export --moments "storage/cache/<Project_Name>/moments.json"`
   - Automatically outputs all clips into `storage/output/Project_X/` at ~8 to 10 seconds per clip.
