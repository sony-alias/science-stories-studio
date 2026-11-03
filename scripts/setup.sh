#!/usr/bin/env bash
# Prepares a fresh Linux workspace to render Science Stories videos. Safe to run more than once.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== system packages"
if ! dpkg -s libpango1.0-dev dvisvgm texlive-latex-extra fonts-urw-base35 >/dev/null 2>&1; then
  sudo_cmd=""; [ "$(id -u)" -ne 0 ] && sudo_cmd="sudo"
  $sudo_cmd apt-get update -q >/dev/null
  $sudo_cmd apt-get install -y -q libpango1.0-dev libcairo2-dev pkg-config dvisvgm texlive-latex-extra \
      fonts-urw-base35 >/dev/null
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }

echo "== python packages"
python3 -c "import manim, kokoro_onnx, soundfile" 2>/dev/null || \
  pip install -q --break-system-packages manim kokoro-onnx soundfile

echo "== narration voice (Kokoro, offline)"
mkdir -p kokoro
base=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s kokoro/kokoro-v1.0.onnx ] || curl -sL -o kokoro/kokoro-v1.0.onnx "$base/kokoro-v1.0.onnx"
[ -s kokoro/voices-v1.0.bin ] || curl -sL -o kokoro/voices-v1.0.bin "$base/voices-v1.0.bin"

echo "== check"
python3 - <<'PY'
import os, sys
sys.path.insert(0, "kit")
os.environ.setdefault("KOKORO_DIR", os.path.abspath("kokoro"))
import worlds_of_flow as w
p, d = w.speak("Setup check.")
print("voice ok,", round(d, 2), "s")
PY
echo "ready"
