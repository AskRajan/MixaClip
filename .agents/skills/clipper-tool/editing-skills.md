# Video Editing Skills & Specifications (`editing-skills.md`)

This document defines the strict, standard production pipeline for turning gaming gameplay videos into viral vertical short videos (9:16 layout).

---

## 1. Captions & Language Rule
- **Verbatim Word-by-Word Direct Transcription (Zero AI Paraphrasing / Skips):**
  - Never use AI to summarize, smooth out, or skip words.
  - Every single word the gamer speaks—including ALL filler words (*bhai, yaar, arre, toh, so let's go, oh nice, I know, guys, uh*), slangs, and exclamations—MUST be captured verbatim.
  - Obtain exact word-level millisecond timestamps (e.g. via YouTube auto-captions VTT word tags `<time><c> word</c>` or WhisperX word-alignment).
  - Subtitle timestamps must be relative to the clip (`0.00` to `28.00s`), ensuring 100% synchronization with speech.
- **Language Format:** Strictly **Hinglish** captions (Hindi spoken dialogue transliterated accurately into Roman script).
- **Text Casing:** **Title Case** (First letter of each word capitalized, rest lowercase, e.g. `"Gaadi Lekar Hum"`, `"Nikal Chuke Hain"`). Never all-caps or all-lowercase.
- **Word Chunking:** Strictly **2 to 3 words per event** (Single line, never multi-line). Immediately vanishes as speech advances.
- **Visual Style & Alignment:**
  - **Alignment:** Strictly `center` (horizontally & vertically centered in lower third).
  - **Font Size:** Sleek, decreased readable size (`44px`, `fontWeight: 900`).
  - **Background Box:** **None** (NO black background box, no lining, completely transparent).
  - **Contrast:** Crisp multi-layer drop shadow and black outline (`textShadow: "0 4px 14px rgba(0,0,0,0.95), -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"`).
  - **Animation:** Punchy spring pop (`damping: 12, stiffness: 240, mass: 0.4`) on each 2-3 word phrase entrance to match gamer speech energy.

---

## 2. 9:16 Layout & Video Separation (1080 x 1920)

```
+------------------------------------------+
|                                          |
|        TOP 30% SCREEN (1080 x 576)       |
|    Gamer Facecam Live Reaction Video     |
|                                          |
+------------------------------------------+
|   [ VIRAL HOOK BADGE: 3-4 WORDS ONLY ]   |  <- At 30% boundary (single line, white pill)
+------------------------------------------+
|                                          |
|                                          |
|       BOTTOM 70% SCREEN (1080 x 1344)    |
|             Real Gameplay Video          |
|                                          |
|                                          |
|         [ DYNAMIC SUBTITLES ]            |  <- Lower third
+------------------------------------------+
```

---

## 3. FFmpeg Video Extraction & Cropping Rules

### A. Gamer Facecam Extraction (Top 30% Screen)
From the source 1920x1080 landscape video, detect and crop the gamer webcam box.
* For GTA 6 source videos:
  - **Coordinates:** `x=1524`, `y=126`, `w=367`, `h=225`
  - **FFmpeg Filter:** `crop=367:225:1524:126,scale=1080:576:flags=lanczos`
  - **Audio:** Audio can be included or mapped to avoid multi-audio conflicts.

### B. Real Gameplay Extraction (Bottom 70% Screen)
* From the source 1920x1080 landscape video:
  - **FFmpeg Filter:** `crop=1080:840:420:240,scale=1080:1344:flags=lanczos` (or full center crop scaled to 1080x1344)
  - **Audio:** Original synchronized game + commentary audio track.

---

## 4. Remotion Assembly
- Pass real video paths into `GamerClipTemplate`:
  - `facecamSource`: Path or static URL to the facecam `.mp4`
  - `gameplaySource`: Path or static URL to the gameplay `.mp4`
  - `hookText`: 3–4 words single-line uppercase hook badge
  - `subtitles`: Array of `{ text, startFrame, endFrame }` in Hinglish.
- Audio and video stay 100% in sync at 60 fps.
