"""
Text formatting & ASS timing utilities for MixaClip.
"""

def format_ass_time(seconds: float) -> str:
    """Format seconds into ASS subtitle timestamp format: H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def to_title_case(text: str) -> str:
    """Convert text to clean Title Case for Roman Hinglish."""
    words = text.strip().split()
    return " ".join([w.capitalize() for w in words])
