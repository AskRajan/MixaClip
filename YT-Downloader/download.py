"""
YouTube & Video Downloader
Powered by yt-dlp (https://github.com/yt-dlp/yt-dlp)
Outputs all downloaded videos into the 'video-list' directory.
"""

import sys
import os
import argparse
from pathlib import Path

# Try importing yt_dlp, or fall back to informing user
try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


def get_output_dir() -> Path:
    """Locate or create the target 'video-list' directory."""
    script_dir = Path(__file__).resolve().parent

    # Check sibling directory (e.g. Cliper/video-list)
    sibling_dir = script_dir.parent / "video-list"
    # Check local directory (e.g. YT-Downloader/video-list)
    local_dir = script_dir / "video-list"

    if sibling_dir.exists():
        return sibling_dir
    elif local_dir.exists():
        return local_dir
    else:
        # Default to sibling if in subfolder, else local
        target = sibling_dir if script_dir.parent.name else local_dir
        target.mkdir(parents=True, exist_ok=True)
        return target


def download_video(url: str, output_dir: Path, audio_only: bool = False, quality: str = "best"):
    """Download a single video or playlist URL into output_dir."""
    url = url.strip()
    if not url or url.startswith("#"):
        return

    print(f"\n[+] Starting download for: {url}")
    print(f"[+] Output folder: {output_dir}")

    outtmpl = str(output_dir / "%(title)s [%(id)s].%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "noplaylist": False,
        "ignoreerrors": True,
        "progress_hooks": [],
    }

    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        # Default to 1080p @ 60fps (or best <=1080p available) merged into mp4
        ydl_opts.update({
            "format": "bestvideo[height<=1080][fps>=50][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080][fps>=50]+bestaudio/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
            "merge_output_format": "mp4",
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download([url])
            if retcode == 0:
                print(f"[SUCCESS] Download completed for: {url}")
            else:
                print(f"[WARNING] Download finished with code {retcode} for: {url}")
    except Exception as e:
        print(f"[ERROR] Failed to download {url}: {e}")


def main():
    output_dir = get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="Download videos directly to video-list folder using yt-dlp.")
    parser.add_argument("url", nargs="?", help="URL of the video or playlist to download")
    parser.add_argument("-f", "--file", help="Path to text file containing URLs (one per line)")
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only (MP3 format)")
    parser.add_argument("-o", "--output", help="Custom output directory (default: video-list)")

    args = parser.parse_args()

    target_dir = Path(args.output).resolve() if args.output else output_dir

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[ERROR] File not found: {args.file}")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        print(f"[+] Loaded {len(urls)} URL(s) from {args.file}")
        for url in urls:
            download_video(url, target_dir, audio_only=args.audio)
    elif args.url:
        download_video(args.url, target_dir, audio_only=args.audio)
    else:
        # Interactive prompt mode
        print("==================================================")
        print("           YT-Downloader (yt-dlp)                 ")
        print("==================================================")
        print(f"Target folder for downloads: {target_dir}")
        print("Paste a video/playlist URL, or press Enter to read from 'urls.txt':")
        user_input = input(">> ").strip()

        if user_input:
            download_video(user_input, target_dir, audio_only=args.audio)
        else:
            default_txt = Path(__file__).resolve().parent / "urls.txt"
            if default_txt.exists():
                with open(default_txt, "r", encoding="utf-8") as f:
                    urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
                if urls:
                    print(f"[+] Found {len(urls)} URL(s) in urls.txt")
                    for url in urls:
                        download_video(url, target_dir, audio_only=args.audio)
                else:
                    print("urls.txt is empty. Add URLs into urls.txt or run with: python download.py <URL>")
            else:
                print("No URL provided and urls.txt was not found.")


if __name__ == "__main__":
    main()
