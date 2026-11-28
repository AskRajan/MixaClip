"""
Transcriber module for MixaClip.
Extracts audio and generates verbatim word-by-word timestamps via faster-whisper INT8.
"""

import subprocess
from pathlib import Path
from typing import List, Dict
from mixaclip.utils.system_check import find_ffmpeg

def extract_audio_wav(video_path: Path, output_audio: Path) -> Path:
    """Extract audio track as 16kHz mono WAV for fast Whisper transcription."""
    ffmpeg_bin = find_ffmpeg()
    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_audio)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_audio

def transcribe_audio(audio_path: Path, model_root: Path = None) -> List[Dict]:
    """Transcribe audio using faster-whisper INT8 with verbatim word timestamps."""
    from faster_whisper import WhisperModel
    print("[*] Loading faster-whisper 'small' model (INT8 CPU)...")
    download_root = str(model_root) if model_root else None
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=download_root)

    prompt = "Hindi spoken dialogue in Roman Hinglish script: bhai, yaar, arre, gaadi, police, dekho, kya, chal, ruk, jaldi, oh bhai, wait"

    print(f"[*] Transcribing audio: {audio_path.name}...")
    segments, _ = model.transcribe(
        str(audio_path),
        beam_size=5,
        word_timestamps=True,
        initial_prompt=prompt,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    all_words = []
    for segment in segments:
        if not segment.words:
            continue
        for word in segment.words:
            clean_word = word.word.strip()
            if clean_word:
                all_words.append({
                    "word": clean_word,
                    "start": round(word.start, 3),
                    "end": round(word.end, 3),
                    "probability": round(word.probability, 3)
                })

    return all_words
