"""
Aspect Ratio Utility for MixaClip.
Strictly ensures zero stretching or squishing on video inputs.
"""

def get_proportional_filter(width: int, height: int) -> str:
    """
    Returns an FFmpeg filter snippet that proportionally scales input to fill
    the given dimensions and crops any excess, preserving the native aspect ratio.
    """
    return f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1"
