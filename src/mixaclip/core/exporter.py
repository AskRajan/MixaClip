"""
Native FFmpeg Ultra-Fast Compositor & Exporter for MixaClip.
Exports vertical shorts directly into storage/output/Project_X/.
"""

import json
import re
import subprocess
import time
from pathlib import Path
from mixaclip.utils.system_check import find_ffmpeg
from mixaclip.templates.split_screen import generate_split_screen_ass, get_split_screen_filtergraph

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_OUTPUT_BASE = ROOT_DIR / "storage" / "output"
CLIPS_DIR = ROOT_DIR / "clipper-tool" / "public" / "clips"

def get_next_project_dir(output_base: Path = DEFAULT_OUTPUT_BASE) -> Path:
    output_base.mkdir(parents=True, exist_ok=True)
    existing = [d for d in output_base.iterdir() if d.is_dir() and d.name.startswith("Project_")]
    if not existing:
        next_dir = output_base / "Project_1"
    else:
        indices = []
        for d in existing:
            m = re.search(r'Project_(\d+)', d.name)
            if m:
                indices.append(int(m.group(1)))
        next_idx = max(indices) + 1 if indices else 1
        next_dir = output_base / f"Project_{next_idx}"
    next_dir.mkdir(parents=True, exist_ok=True)
    return next_dir

def export_clips(moments_file: Path, project_dir: Path = None, width=720, height=1280, fps=30, template=1):
    ffmpeg_bin = find_ffmpeg()
    if not ffmpeg_bin:
        raise RuntimeError("FFmpeg binary not found. Please install FFmpeg or place in bin/ffmpeg/bin/.")

    with open(moments_file, "r", encoding="utf-8") as f:
        moments = json.load(f)

    if project_dir is None:
        project_dir = get_next_project_dir()
    project_dir.mkdir(parents=True, exist_ok=True)

    print("================================================================")
    print("       MIXA-CLIP ULTRA-FAST DIRECT FFMPEG PIPELINE              ")
    print("================================================================")
    print(f"Target Output Folder: {project_dir}")
    print(f"Resolution: {width}x{height} @ {fps}fps | Template: {template}\n")

    face_h = int(height * 0.30)
    game_h = height - face_h

    total_time = 0.0
    exported_files = []

    # Temporary directory for ASS files
    temp_ass_dir = project_dir / ".temp_ass"
    temp_ass_dir.mkdir(parents=True, exist_ok=True)

    for idx, m in enumerate(moments, start=1):
        hook = m.get("hook_heading", f"MOMENT {idx}")
        face_in = CLIPS_DIR / f"clip{idx}_face.mp4"
        game_in = CLIPS_DIR / f"clip{idx}_game.mp4"

        ass_file = temp_ass_dir / f"clip{idx}.ass"
        out_file = project_dir / f"clip_0{idx}_{width}p{fps}.mp4"

        generate_split_screen_ass(m, ass_file, width=width, height=height)

        filtergraph = get_split_screen_filtergraph(
            width=width,
            height=height,
            face_h=face_h,
            game_h=game_h,
            ass_filename=ass_file.name
        )

        cmd = [
            ffmpeg_bin, "-y",
            "-i", str(face_in),
            "-i", str(game_in),
            "-filter_complex", filtergraph,
            "-map", "[outv]",
            "-map", "1:a?",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "20",
            "-r", str(fps),
            "-c:a", "aac", "-b:a", "192k",
            str(out_file)
        ]

        t0 = time.time()
        res = subprocess.run(cmd, cwd=str(temp_ass_dir), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        elapsed = time.time() - t0

        if res.returncode == 0:
            size_mb = out_file.stat().st_size / (1024 * 1024)
            total_time += elapsed
            exported_files.append((out_file, elapsed, size_mb))
            print(f"[{idx}/{len(moments)}] Clip #{idx} ({hook}) exported in {elapsed:.2f}s ({size_mb:.1f} MB)")
        else:
            print(f"[!] Error on clip #{idx}: {res.stderr}")

    print("\n================================================================")
    print(f"   EXPORT COMPLETE: {len(exported_files)} CLIPS IN {total_time:.2f}s TOTAL!    ")
    print(f"   Saved to: {project_dir}")
    print("================================================================")
    return exported_files
