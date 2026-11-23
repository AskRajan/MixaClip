---
name: yt-downloader
description: Download videos (single, batch, audio) into video-list using yt-dlp.
---

# YT-Downloader Skill

How to operate and use the video downloader in `YT-Downloader/`.

## Destination & Default Quality
- **Target folder:** `video-list/`
- **Default Quality Rule:** Unless user specifies another resolution/framerate, videos must always download in **1080p @ 60fps** (fallback to highest available <=1080p), merged into `.mp4`.

## How to Use

### 1. Python Script
```bash
# Download single video (default: 1080p @ 60fps mp4):
python YT-Downloader/download.py "<URL>"

# Batch download multiple URLs from urls.txt:
python YT-Downloader/download.py -f YT-Downloader/urls.txt

# Extract audio only (MP3 192kbps):
python YT-Downloader/download.py -a "<URL>"
```

### 2. Standalone Binary (`yt-dlp.exe`)
```bash
.\YT-Downloader\yt-dlp.exe -P "video-list" -f "bestvideo[height<=1080][fps>=50][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080][fps>=50]+bestaudio/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" --merge-output-format mp4 -o "%(title)s [%(id)s].%(ext)s" "<URL>"
```

### 3. Windows Batch Launchers (Interactive)
- Root shortcut: `download_video.bat`
- Tool launcher: `YT-Downloader/run_downloader.bat`
Double-clicking prompts for a URL or downloads lines from `urls.txt`.
