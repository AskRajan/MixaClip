"""
Unified CLI Entrypoint for MixaClip.
Usage:
    python -m mixaclip check
    python -m mixaclip run "<YOUTUBE_URL>"
    python -m mixaclip export --moments path/to/moments.json
"""

import argparse
import sys
from pathlib import Path
from mixaclip.utils.system_check import verify_all
from mixaclip.core.exporter import export_clips, get_next_project_dir

def main():
    parser = argparse.ArgumentParser(
        prog="mixaclip",
        description="MixaClip - Automated Gaming Highlights & 9:16 Vertical Shorts Pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: check
    subparsers.add_parser("check", help="Verify local environment, FFmpeg, and Python packages")

    # Command: export
    export_parser = subparsers.add_parser("export", help="Export vertical shorts from approved moments.json")
    export_parser.add_argument("--moments", type=str, required=True, help="Path to moments.json file")
    export_parser.add_argument("--width", type=int, default=720, help="Output width (default: 720)")
    export_parser.add_argument("--height", type=int, default=1280, help="Output height (default: 1280)")
    export_parser.add_argument("--fps", type=int, default=30, help="Output framerate (default: 30)")
    export_parser.add_argument("--template", type=int, default=1, help="Template index (default: 1)")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run full pipeline from YouTube URL")
    run_parser.add_argument("url", type=str, help="YouTube video URL")
    run_parser.add_argument("--quality", type=str, default="720p30", choices=["720p30", "720p", "1080p", "1080p60"])

    args = parser.parse_args()

    if args.command == "check":
        ok = verify_all()
        sys.exit(0 if ok else 1)

    elif args.command == "export":
        moments_p = Path(args.moments).resolve()
        if not moments_p.exists():
            print(f"[!] Error: Moments file not found at {moments_p}")
            sys.exit(1)
        p_dir = get_next_project_dir()
        export_clips(moments_p, project_dir=p_dir, width=args.width, height=args.height, fps=args.fps, template=args.template)

    elif args.command == "run":
        from mixaclip.core.downloader import download_video
        print(f"[*] Starting MixaClip pipeline for: {args.url}")
        verify_all()
        download_video(args.url, quality=args.quality)
        print("[*] Download complete. Next step: analyze moments and export.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
