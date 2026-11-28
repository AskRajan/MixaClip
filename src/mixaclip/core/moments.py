"""
Moment detection & scoring module for MixaClip.
Identifies high-energy, viral 25-30s windows with catchy hook badges.
"""

from pathlib import Path
from typing import List, Dict
from mixaclip.utils.text_formatter import to_title_case

KEYWORDS = {
    "bhai": 3.0, "yaar": 2.5, "arre": 3.0, "wait": 3.0, "police": 2.5,
    "gaadi": 2.0, "oh": 2.5, "kya": 2.0, "bhaag": 3.5, "dekho": 2.0,
    "mar": 2.5, "bach": 3.0, "clutch": 4.0, "no": 2.0, "omg": 3.5,
    "jaldi": 2.5, "thuk": 3.0, "khatarnak": 3.0, "ruk": 2.0
}

def detect_scenes(video_path: Path) -> List[float]:
    """Detect visual cut timestamps using PySceneDetect."""
    try:
        from scenedetect import detect, ContentDetector
        print(f"[*] Running scene detection on {video_path.name}...")
        scene_list = detect(str(video_path), ContentDetector(threshold=27.0))
        return [scene[0].get_seconds() for scene in scene_list]
    except Exception as e:
        print(f"[!] PySceneDetect warning: {e}")
        return []

def build_word_chunks(words: List[Dict], chunk_size: int = 3) -> List[Dict]:
    """Group words into rapid 2-3 word chunks in Title Case."""
    chunks = []
    i = 0
    while i < len(words):
        group = words[i:i + chunk_size]
        text = to_title_case(" ".join([w["word"] for w in group]))
        chunks.append({
            "text": text,
            "start": group[0]["start"],
            "end": group[-1]["end"]
        })
        i += chunk_size
    return chunks

def identify_viral_moments(all_words: List[Dict], scene_times: List[float], video_duration: float, count: int = 5, duration: float = 28.0) -> List[Dict]:
    """Score candidate time windows for highest speech density & reaction score."""
    step = 5.0
    candidates = []
    
    t = 0.0
    while t + duration <= video_duration:
        t_end = t + duration
        words_in_window = [w for w in all_words if t <= w["start"] <= t_end]
        
        score = 0.0
        # Word density
        score += len(words_in_window) * 0.5
        # Reaction keywords
        for w in words_in_window:
            lower = w["word"].lower().strip("!?,.")
            if lower in KEYWORDS:
                score += KEYWORDS[lower]
        # Scene cuts
        scenes_in_window = [st for st in scene_times if t <= st <= t_end]
        score += min(len(scenes_in_window) * 1.5, 9.0)

        candidates.append({
            "start": round(t, 2),
            "end": round(t_end, 2),
            "score": round(score, 2),
            "words": words_in_window
        })
        t += step

    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Pick non-overlapping moments
    selected = []
    for c in candidates:
        if len(selected) >= count:
            break
        overlap = False
        for s in selected:
            if not (c["end"] <= s["start"] + 10 or c["start"] >= s["end"] - 10):
                overlap = True
                break
        if not overlap:
            selected.append(c)

    selected.sort(key=lambda x: x["start"])

    # Build final formatted moments
    final_moments = []
    for idx, m in enumerate(selected, start=1):
        rel_words = []
        for w in m["words"]:
            rel_words.append({
                "word": w["word"],
                "start": max(0.0, round(w["start"] - m["start"], 3)),
                "end": max(0.1, round(w["end"] - m["start"], 3)),
                "probability": w.get("probability", 1.0)
            })
        
        chunks = build_word_chunks(rel_words, chunk_size=3)
        sample_text = " ".join([w["word"] for w in m["words"][:6]])
        hook_heading = to_title_case(sample_text[:25]).upper()

        final_moments.append({
            "clip_id": idx,
            "start_time": m["start"],
            "end_time": m["end"],
            "duration_seconds": duration,
            "hook_heading": hook_heading,
            "score": m["score"],
            "chunks_3s": chunks
        })

    return final_moments
