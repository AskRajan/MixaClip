---
name: setup
description: Set up, configure, and verify the Cliper local development environment on a new machine.
---

# Cliper Local Setup Skill

Guide and automated procedure for an agent to set up the Cliper repository on a user's local machine after cloning.

## Prerequisites Check

Before starting, verify the following runtimes on the host machine:
1. **Python 3.10+**: `python --version`
2. **Node.js 18+ & npm**: `node --version` and `npm --version`
3. **FFmpeg 7.x**: Check `Clipper Tool/ffmpeg/bin/ffmpeg.exe` or system `ffmpeg -version`.

---

## Step-by-Step Setup Procedure

### Step 1: Create Python Virtual Environment (`venv`)
Inside the `Clipper Tool/` directory, set up the dedicated Python virtual environment:

```powershell
cd "Clipper Tool"
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.\venv\Scripts\activate.bat`
- **macOS / Linux:** `source venv/bin/activate`

### Step 2: Install Python Dependencies
Install required packages using the virtual environment's pip:

```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```
*Packages installed: `faster-whisper`, `scenedetect[opencv]`, and `yt-dlp`.*

### Step 3: Install Node.js & Remotion Dependencies
Inside `Clipper Tool/`, install the Remotion 4.x dependencies:

```powershell
cd "Clipper Tool"
npm install
```

### Step 4: Verify or Download FFmpeg
Check if FFmpeg binary exists in `Clipper Tool/ffmpeg/bin/ffmpeg.exe` or globally on PATH:
- If missing on Windows:
  Download the FFmpeg release essentials build (or use `winget install Gyan.FFmpeg`) and ensure `ffmpeg.exe` is placed at `Clipper Tool/ffmpeg/bin/ffmpeg.exe` or accessible via PATH.

### Step 5: Verify or Download `yt-dlp`
Check if `YT-Downloader/yt-dlp.exe` exists or yt-dlp is available:
- If missing on Windows:
  Download the latest `yt-dlp.exe` to `YT-Downloader/` via:
  ```powershell
  python -m pip install --upgrade yt-dlp
  ```
  Or fetch the standalone binary directly into `YT-Downloader/yt-dlp.exe`.

### Step 6: Create Required Workspace Directories
Ensure all necessary runtime folders exist:
- `video-list/` (for downloaded videos)
- `projects/` (for local video clipping projects)
- `Clipper Tool/public/clips/` (for Remotion static asset preview)

---

## Verification & Health Check

Run these quick checks to ensure everything is operational:

1. **Verify Python packages:**
   ```powershell
   .\Clipper Tool\venv\Scripts\python.exe -c "import faster_whisper, scenedetect; print('Python AI Stack OK')"
   ```
2. **Verify Remotion Studio Preview:**
   ```powershell
   cd "Clipper Tool"
   npx remotion preview remotion/src/index.ts --port=3000
   ```
3. **Verify Downloader:**
   ```powershell
   python YT-Downloader/download.py --help
   ```

When all 3 checks pass, the local environment is 100% ready for clipping workflow.
