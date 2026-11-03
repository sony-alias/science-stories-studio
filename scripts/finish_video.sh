#!/usr/bin/env bash
# Normalise a rendered Manim video's narration to YouTube loudness without re-encoding the picture.
# Usage: scripts/finish_video.sh RENDERED.mp4 FINAL.mp4
set -euo pipefail
ffmpeg -v error -y -i "$1" -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k \
  -movflags +faststart "$2"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$2"
