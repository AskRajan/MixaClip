# MixaClip
- Media downloads live in `storage/downloads/`.
- Local portable binaries live in `bin/` (FFmpeg, yt-dlp).
- Source package lives in `src/mixaclip/`.
- Master output vertical clips are exported to `storage/output/Project_1/`, `storage/output/Project_2/`, etc.
- Unified command: `python -m mixaclip <command>` (supports `check`, `run`, `export`).
- Aspect ratio rule: Never stretch gameplay video; preserve natural aspect ratio with proportional scaling and center cropping (`force_original_aspect_ratio=increase,crop=...`).
