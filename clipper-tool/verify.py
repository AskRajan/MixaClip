import sys
import subprocess
from pathlib import Path

base_dir = Path(__file__).resolve().parent

print("========================================")
print("     Clipper Tool Verification Check    ")
print("========================================")

# 1. Verify FFmpeg 7.x
ffmpeg_bin = base_dir / "ffmpeg" / "bin" / "ffmpeg.exe"
print(f"[1] Checking FFmpeg at: {ffmpeg_bin}")
try:
    res = subprocess.run([str(ffmpeg_bin), "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    first_line = res.stdout.splitlines()[0] if res.stdout else "Unknown"
    print(f"    -> FFmpeg Output: {first_line}")
    assert "version 7." in first_line, f"Expected FFmpeg 7.x, got: {first_line}"
    print("    [PASS] FFmpeg 7.x is working!")
except Exception as e:
    print(f"    [FAIL] FFmpeg check failed: {e}")
    sys.exit(1)

# 2. Verify Remotion 4.x
print(f"[2] Checking Remotion CLI...")
try:
    remotion_cmd = base_dir / "node_modules" / ".bin" / "remotion.cmd"
    res = subprocess.run([str(remotion_cmd), "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = (res.stdout or res.stderr).strip().splitlines()[0]
    print(f"    -> Remotion Output: {output}")
    assert "4." in output, f"Expected Remotion 4.x, got: {output}"
    print("    [PASS] Remotion 4.x is working!")
except Exception as e:
    print(f"    [FAIL] Remotion check failed: {e}")
    sys.exit(1)

# 3. Verify PySceneDetect 0.6.x
print(f"[3] Checking PySceneDetect...")
try:
    import scenedetect
    sd_version = scenedetect.__version__
    print(f"    -> PySceneDetect version: {sd_version}")
    assert sd_version.startswith("0.6."), f"Expected PySceneDetect 0.6.x, got: {sd_version}"
    print("    [PASS] PySceneDetect 0.6.x is working!")
except Exception as e:
    print(f"    [FAIL] PySceneDetect check failed: {e}")
    sys.exit(1)

# 4. Verify faster-whisper 1.2.x with 'small' model and CPU INT8
print(f"[4] Checking faster-whisper with small model (CPU INT8)...")
try:
    import faster_whisper
    fw_version = faster_whisper.__version__
    print(f"    -> faster-whisper version: {fw_version}")
    assert fw_version.startswith("1.2."), f"Expected faster-whisper 1.2.x, got: {fw_version}"

    # Model download folder inside Clipper Tool
    models_dir = str(base_dir / "models")
    print(f"    -> Initializing WhisperModel('small', device='cpu', compute_type='int8')...")
    model = faster_whisper.WhisperModel("small", device="cpu", compute_type="int8", download_root=models_dir)
    print("    [PASS] faster-whisper small model loaded successfully with CPU INT8!")
except Exception as e:
    print(f"    [FAIL] faster-whisper check failed: {e}")
    sys.exit(1)

print("\n========================================")
print("  ALL 4 DEPENDENCIES VERIFIED WORKING!  ")
print("========================================")
