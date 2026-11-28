"""
Split-Screen Template (Template 1) for MixaClip.
Top 30% Facecam + Center Hook Badge Pill + Bottom 70% Gameplay + Subtitles.
Strictly preserves natural aspect ratio without stretching.
"""

from pathlib import Path
from mixaclip.utils.text_formatter import format_ass_time
from mixaclip.utils.aspect_ratio import get_proportional_filter

def generate_split_screen_ass(moment: dict, ass_path: Path, width=720, height=1280) -> Path:
    hook = moment.get("hook_heading", "VIRAL MOMENT")
    chunks = moment.get("chunks_3s", [])
    dur = moment.get("duration_seconds", 28.0)

    scale_factor = width / 720.0
    sub_font_size = int(34 * scale_factor)
    hook_font_size = int(30 * scale_factor)

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {width}",
        f"PlayResY: {height}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Subtitle,Arial,{sub_font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,2,2,15,15,110,1",
        f"Style: HookBadge,Arial,{hook_font_size},&H00050505,&H000000FF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,1,0,3,10,3,8,20,20,360,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 0,0:00:00.00,{format_ass_time(dur)},HookBadge,,0,0,0,,{{\\b1\\uppercase}}{hook}"
    ]

    for c in chunks:
        t_start = format_ass_time(max(0, c["start"]))
        t_end = format_ass_time(max(c["start"] + 0.3, c["end"]))
        txt = c["text"].replace("\n", " ").strip()
        lines.append(f"Dialogue: 1,{t_start},{t_end},Subtitle,,0,0,0,,{{\\b1}}{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return ass_path

def get_split_screen_filtergraph(width: int, height: int, face_h: int, game_h: int, ass_filename: str) -> str:
    face_filter = get_proportional_filter(width, face_h)
    game_filter = get_proportional_filter(width, game_h)
    
    return (
        f"[0:v]{face_filter}[face];"
        f"[1:v]{game_filter}[game];"
        f"[face][game]vstack=inputs=2[stacked];"
        f"[stacked]ass={ass_filename}[outv]"
    )
