"""
Downloader module for MixaClip.
Wraps yt-dlp to download footage into storage/downloads/ with quality selection.
"""

import sys
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DOWNLOADS_DIR = ROOT_DIR / "storage" / "downloads"
BIN_YTDLP = ROOT_DIR / "bin" / "yt-dlp.exe"

def find_ytdlp() -> str:
    if BIN_YTDLP.exists():
        return str(BIN_YTDLP)
    legacy = ROOT_DIR / "YT-Downloader" / "yt-dlp.exe"
    if legacy.exists():
        return str(legacy)
    system_ytdlp = shutil.which("yt-dlp")
    if system_ytdlp:
        return system_ytdlp
    return sys.executable + " -m yt_dlp"

def download_video(url: str, output_dir: Path = DOWNLOADS_DIR, quality: str = "720p30") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ytdlp = find_ytdlp()

    # Format string based on requested quality
    if quality == "1080p60":
        fmt = "bestvideo[height<=1080][fps>=50]+bestaudio/best[height<=1080]"
    elif quality == "1080p":
        fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    elif quality == "720p":
        fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    else:  # default 720p30 / fast
        fmt = "bestvideo[height<=720][fps<=30]+bestaudio/best[height<=720]"

    out_tmpl = str(output_dir / "%(title)s [%(id)s].%(ext)s")
    cmd = [
        ytdlp,
        "-f", fmt,
        "--merge-output-format", "mp4",
        "-o", out_tmpl,
        url
    ]

    print(f"Downloading {url} to {output_dir} (Quality: {quality})...")
    subprocess.check_call(cmd)
    
    # Return downloaded mp4 files
    mp4s = sorted(output_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if mp4s:
        return mp4s[0]
    return output_dir
