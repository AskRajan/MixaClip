---
name: clipper-tool
description: Transcribe gamer MP4 videos, identify best moments, present timestamps for user approval, and edit clips.
---

# Clipper Tool Workflow

Process gamer MP4 videos into high-engagement vertical shorts using `Clipper Tool/`.

## Stack
- **Whisper:** `Clipper Tool/venv` (`faster-whisper` `small` model, CPU INT8)
- **Scenes:** `PySceneDetect`
- **Video & Editing:** `Clipper Tool/ffmpeg/bin/ffmpeg.exe`, `Remotion 4.x`
- **Locked Template:** `Clipper Tool/remotion/src/GamerClip.tsx` (immutable)
- **Editing Specification:** Refer to `editing-skills.md` for exact facecam cropping, gameplay scaling, and Hinglish rules.

## Output Organization
All work for a video is isolated in `projects/[video_name]/`:
- `projects/[video_name]/transcript.json` (strictly Hinglish subtitles in 2-3 word audio-synced intervals)
- `projects/[video_name]/final_shorts/*.mp4`
The core template and tools are never modified.

## Procedure (5-Step Execution Workflow)

1. **Step 1: Receive Video URL & Quality Selection (Download Gate):**
   - Input: Video URL provided by the user.
   - **Quality Check:**
     - If the user explicitly specified resolution/FPS (e.g., 720p, 1080p, 4K), use that directly (download 4K if system hardware/format supports it).
     - If quality is **not** specified, **ask the user** to choose:
       * *Option 1: 720p @ 60fps*
       * *Option 2: 1080p @ 60fps*
   - Download the video into `video-list/` via `YT-Downloader/download.py "<URL>"`.

2. **Step 2: Language Check:**
   - If user specified a language, use it.
   - If user did **not** mention a language, **ask the user** before proceeding:
     * *Option 1: Pure English*
     * *Option 2: Hinglish (Hindi + English)*

3. **Step 3: Extract Verbatim Transcript & Identify Viral Moments (Combined Step):**
   - **Transcript Generation (Strict Verbatim SOP):**
     - Zero AI paraphrasing/summarization (100% verbatim, retain all filler words like *bhai, yaar, arre*, slangs, and reactions).
     - Forced word-level millisecond alignment.
     - Hinglish Roman script, Title Case, strictly 2-3 words per screen, center aligned 44px with spring pop entrance.
     - Saved in `projects/[video_name]/transcript.json`.
   - **Viral Moments Selection & Approval Gate 1:**
     - Ask user for desired clip count: **2, 5, 10, or 15 clips**.
     - Concurrently analyze transcript and scene changes for crazy gamer reactions, fight scenes, clutch moments, and viral hooks.
     - Present proposed moments (start/end time, duration 25–30s, transcript text, viral hook badge) for user approval.
     - **WAIT:** No video editing or cutting begins until user approves the proposed moments.

4. **Step 4: Build Clips & Interactive Browser Preview (Approval Gate 2):**
   - Once moments are approved, configure them in Remotion Studio.
   - Serve live interactive preview at `http://localhost:3000`.
   - User reviews playback, hook badges, and subtitle timing. Apply any requested adjustments.

5. **Step 5: Final MP4 Export (Strict Permission Rule):**
   - **NEVER export automatically.**
   - Only when user explicitly commands export (e.g., *"एक्सपोर्ट करो"* / *"रेंडर करो"*), execute headless render:
     ```bash
     npx remotion render GamerClipShort "projects/[video_name]/final_shorts/clip_01.mp4" --props='...'
     ```
   - Target format: 9:16 vertical (`1080x1920` @ 60fps), 25–30 seconds.
