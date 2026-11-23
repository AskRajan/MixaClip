@echo off
setlocal enabledelayedexpansion
title YT-Downloader

cd /d "%~dp0"

echo ======================================================
echo             YT-Downloader (yt-dlp)
echo      Downloads will be saved in "video-list"
echo ======================================================
echo.

set OUTPUT_DIR=..\video-list
if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

if "%~1"=="" (
    set /p VIDEO_URL="Enter Video/Playlist URL (or press ENTER to download from urls.txt): "
) else (
    set VIDEO_URL=%~1
)

if "!VIDEO_URL!"=="" (
    if exist "urls.txt" (
        echo Reading URLs from urls.txt...
        if exist "yt-dlp.exe" (
            yt-dlp.exe -P "%OUTPUT_DIR%" -a "urls.txt" -f "bestvideo[height<=1080][fps>=50][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080][fps>=50]+bestaudio/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" --merge-output-format mp4 -o "%%(title)s [%%(id)s].%%(ext)s"
        ) else (
            python download.py -f urls.txt
        )
    ) else (
        echo No URL provided and urls.txt not found.
    )
) else (
    echo Downloading "!VIDEO_URL!" (1080p @ 60fps default)...
    if exist "yt-dlp.exe" (
        yt-dlp.exe -P "%OUTPUT_DIR%" "!VIDEO_URL!" -f "bestvideo[height<=1080][fps>=50][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080][fps>=50]+bestaudio/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" --merge-output-format mp4 -o "%%(title)s [%%(id)s].%%(ext)s"
    ) else (
        python download.py "!VIDEO_URL!"
    )
)

echo.
echo ======================================================
echo Download task finished! Check the "video-list" folder.
echo ======================================================
pause
