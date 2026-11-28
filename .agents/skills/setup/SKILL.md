---
name: setup
description: Set up, configure, and verify the Cliper local development environment on a new machine.
---

# MixaClip Local Setup Skill

Guide and automated procedure for an agent to set up the MixaClip repository on a user's local machine after cloning.

## Prerequisites Check

Before starting, verify the following runtimes on the host machine:
1. **Python 3.10+**: `python --version`
2. **FFmpeg 7.x+**: Check `bin/ffmpeg/bin/ffmpeg.exe` or system `ffmpeg -version`.
3. (Optional) **yt-dlp**: Check `bin/yt-dlp.exe` or system PATH.

---

## Step-by-Step Setup Procedure

### Step 1: Create Python Virtual Environment (`venv`)
Inside the repository root directory, set up the Python virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.\venv\Scripts\activate.bat`
- **macOS / Linux:** `source venv/bin/activate`

### Step 2: Install Python Dependencies & Package
Install required packages using the virtual environment's pip:

```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\pip.exe install -e .
```
*Packages installed: `faster-whisper`, `scenedetect[opencv]`, and `yt-dlp`.*

### Step 3: Verify FFmpeg
Check if FFmpeg binary exists in `bin/ffmpeg/bin/ffmpeg.exe` or globally on PATH:
- If missing on Windows:
  Download the FFmpeg release essentials build (or use `winget install Gyan.FFmpeg`) and ensure `ffmpeg.exe` is placed at `bin/ffmpeg/bin/ffmpeg.exe` or accessible via PATH.

### Step 4: Verify `yt-dlp`
Check if `bin/yt-dlp.exe` exists or yt-dlp is available via python.

---

## Verification & Health Check

Run these quick checks to ensure everything is operational:

```powershell
.\venv\Scripts\python.exe -m mixaclip check
```

When this check passes, the local environment is 100% ready for clipping workflow.
