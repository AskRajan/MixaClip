# MixaClip

An automated video clipping and rendering engine designed for gaming creators. MixaClip ingests long-form gameplay footage, detects high-retention viral moments, generates millisecond-accurate word-level verbatim subtitles, and programmatically renders 9:16 vertical Shorts using Remotion and FFmpeg.

---

## Architecture & Stack

MixaClip combines lightweight local AI models with programmatic video compositing:

- **Video Ingestion:** `yt-dlp` (customizable resolutions and frame rates, up to 1080p @ 60fps / 4K).
- **Speech Recognition:** `faster-whisper` (`small` model, CPU INT8 quantized) for millisecond-level word timestamp alignment without audio drift.
- **Scene Detection:** `PySceneDetect` (content-aware cut and scene change detection).
- **Video Slicing & Preprocessing:** `FFmpeg 7.x` (lossless cutting, stream extraction, facecam cropping).
- **Shorts Rendering Engine:** `Remotion 4.x` (React-based declarative video composition at 1080x1920 @ 60fps).

---

## Layout & Subtitle Specifications

Every rendered clip follows a locked composition standard optimized for TikTok, YouTube Shorts, and Instagram Reels:

### 1. Visual Composition (9:16 Vertical — 1080x1920)
- **Top 30% Area:** Gamer Facecam (`object-fit: cover`, centered alignment).
- **Middle Hook Badge:** Dynamic 3–4 word viral hook heading rendered inside a high-contrast pill badge between facecam and gameplay.
- **Bottom 70% Area:** Scaled gameplay footage (`object-fit: cover`, centered).

### 2. Subtitle Formatting (Verbatim SOP)
- **Zero AI Paraphrasing:** 100% verbatim transcription. Preserves all gamer filler words (*bhai, yaar, arre, toh, uh, etc.*), slang, and unfinished dialogue.
- **Chunking:** Strictly 2 to 3 words per screen, rendered on a single line.
- **Typography:** 44px, Font Weight 900, pure white (`#FFFFFF`) with a clean 2px black stroke and drop shadow (no background box).
- **Animation:** Synchronized spring-pop entrance on word transition.
- **Language Support:** Hinglish (Hindi transcribed into Roman script) or Pure English.

---

## Execution Pipeline

The processing workflow incorporates two explicit user-approval gates before any irreversible file operations or heavy rendering occur:

```
[Video Input URL]
       │
       ▼
[Quality Gate] ──► (Verify resolution: 720p@60 / 1080p@60 / 4K)
       │
       ▼
[Language Gate] ──► (Pure English or Roman Hinglish)
       │
       ▼
[Extraction & Analysis] ──► (Verbatim Whisper transcript + PySceneDetect analysis)
       │
       ▼
[Approval Gate 1] ──► (User selects count: 2, 5, 10, or 15 clips; approves timestamps & hook titles)
       │
       ▼
[Remotion Studio Preview] ──► (Interactive browser review at http://localhost:3000)
       │
       ▼
[Approval Gate 2] ──► (User requests adjustments or confirms export)
       │
       ▼
[Headless Render] ──► (1080x1920 @ 60fps MP4 export to projects/[video_name]/final_shorts/)
```

---

## Directory Structure

```
MixaClip/
├── .agents/
│   └── skills/
│       ├── clipper-tool/     # Main clipping workflow definition (SKILL.md)
│       ├── setup/            # Automated machine setup guide (SKILL.md)
│       └── yt-downloader/    # Downloader CLI operational guide (SKILL.md)
├── Clipper Tool/
│   ├── ffmpeg/               # Local FFmpeg 7.x binaries (bin/ffmpeg.exe)
│   ├── remotion/             # Remotion React project root
│   │   └── src/
│   │       ├── GamerClip.tsx # Immutable video composition template
│   │       ├── Root.tsx      # Composition registry & props mapping
│   │       ├── index.ts      # Remotion entry point
│   │       └── clipsData.json
│   ├── public/               # Static assets & sliced media previews
│   ├── package.json          # Node dependencies (Remotion 4.x)
│   └── requirements.txt      # Python dependencies
├── YT-Downloader/            # Video download scripts & yt-dlp binary
├── video-list/               # Local staging folder for downloaded source videos
├── projects/                 # Local workspace for video transcripts, slices, and renders
├── AGENTS.md                 # Agent guidelines and workspace rules
└── .gitignore
```

---

## Installation & Setup

### Prerequisites
- **Python:** 3.10 or higher
- **Node.js:** 18.0.0 or higher (with npm)
- **FFmpeg:** 7.x (available on system PATH or inside `Clipper Tool/ffmpeg/bin/`)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mixaclip.git
cd mixaclip
```

### 2. Set Up Python Environment
Create and activate a virtual environment inside `Clipper Tool/`:

```bash
cd "Clipper Tool"
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Install Remotion Dependencies
Within the `Clipper Tool/` directory:
```bash
npm install
```

### 4. Verify External Tools
- **yt-dlp:** Ensure `YT-Downloader/yt-dlp.exe` is present or install globally via `pip install yt-dlp`.
- **FFmpeg:** Verify FFmpeg via `ffmpeg -version`.

---

## Usage

### 1. Download Source Video
Download a target gaming video into `video-list/` (defaults to 1080p @ 60fps):
```bash
python YT-Downloader/download.py "<YOUTUBE_URL>"
```

### 2. Start Remotion Preview Server
Preview compositions, verify subtitle sync, and inspect framing live in the browser:
```bash
cd "Clipper Tool"
npx remotion preview remotion/src/index.ts --port=3000
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Render Final Shorts (Headless)
Export an approved composition to vertical MP4:
```bash
cd "Clipper Tool"
npx remotion render GamerClipShort "projects/[video_name]/final_shorts/clip_01.mp4" --props='...'
```
