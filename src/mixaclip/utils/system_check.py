"""
System environment check for MixaClip.
Verifies FFmpeg, PySceneDetect, and faster-whisper.
"""

import sys
import shutil
import subprocess
from pathlib import Path

def find_ffmpeg() -> str:
    """Find FFmpeg binary in bin/ or system PATH."""
    root = Path(__file__).resolve().parent.parent.parent.parent
    local_bin = root / "bin" / "ffmpeg" / "bin" / "ffmpeg.exe"
    if local_bin.exists():
        return str(local_bin)
    
    clipper_bin = root / "clipper-tool" / "ffmpeg" / "bin" / "ffmpeg.exe"
    if clipper_bin.exists():
        return str(clipper_bin)
        
    system_bin = shutil.which("ffmpeg")
    if system_bin:
        return system_bin
    return ""

def verify_all():
    print("========================================")
    print("      MixaClip System Verification      ")
    print("========================================")
    
    # 1. FFmpeg
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("[FAIL] FFmpeg binary not found in bin/ or system PATH!")
        return False
    try:
        out = subprocess.check_output([ffmpeg_path, "-version"], text=True)
        print(f"[PASS] FFmpeg found: {out.splitlines()[0]}")
    except Exception as e:
        print(f"[FAIL] FFmpeg execution error: {e}")
        return False

    # 2. PySceneDetect
    try:
        import scenedetect
        print(f"[PASS] PySceneDetect {scenedetect.__version__} is ready.")
    except ImportError:
        print("[FAIL] PySceneDetect is not installed!")
        return False

    # 3. faster-whisper
    try:
        import faster_whisper
        print(f"[PASS] faster-whisper {faster_whisper.__version__} is ready.")
    except ImportError:
        print("[FAIL] faster-whisper is not installed!")
        return False

    print("\n[SUCCESS] All core dependencies verified and operational!")
    return True

if __name__ == "__main__":
    if not verify_all():
        sys.exit(1)
