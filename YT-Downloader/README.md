# YT-Downloader

Video downloader powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).
All downloaded videos are automatically saved into the `video-list/` folder.

> **Default Quality:** Videos download in **1080p @ 60fps** (or highest available <=1080p) merged into `.mp4` format if no specific quality is provided.

---

## 🚀 How to Use

### Method 1: Double-Click Launcher (Easiest)
- Run `run_downloader.bat` inside this folder (or `download_video.bat` in the root).
- Paste any video/playlist URL and press **Enter**.
- The video will be downloaded into `video-list/`.

### Method 2: Batch Download via `urls.txt`
1. Open `urls.txt`.
2. Paste multiple video URLs (one per line).
3. Run `run_downloader.bat` and press **Enter** without typing a URL.

### Method 3: Command Line (Python)
```bash
# Single video:
python download.py "https://www.youtube.com/watch?v=..."

# Batch download from urls.txt:
python download.py -f urls.txt

# Audio only (MP3):
python download.py -a "https://www.youtube.com/watch?v=..."
```

### Method 4: Standalone Executable (`yt-dlp.exe`)
```bash
.\yt-dlp.exe -P "..\video-list" -o "%(title)s [%(id)s].%(ext)s" "<URL>"
```
