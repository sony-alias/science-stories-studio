#!/usr/bin/env bash
# Store finished video files on their own branch, video/<NAME>, so main stays small and quick to clone.
# Each branch holds one commit with just those files. GitHub plays or downloads them from the link printed.
# Usage: scripts/store_video.sh NAME FILE [FILE...]      e.g. scripts/store_video.sh I005 out/I005.mp4 out/I005_thumb.png
# Branch names cannot be reused or deleted from a session, so use a new NAME each time (IdeaID-YYYYMMDD).
# Keep each call under about 50 MB in total; split bigger sets over several calls.
set -euo pipefail
[ $# -ge 2 ] || { sed -n 2,5p "$0"; exit 1; }
name="$1"; shift
repo="$(cd "$(dirname "$0")/.." && pwd)"
remote="$(git -C "$repo" remote get-url origin)"
slug="$(echo "$remote" | sed -E 's#(https://github.com/|git@github.com:)##; s#\.git$##')"
for f in "$@"; do
  size=$(stat -c %s "$f")
  [ "$size" -lt 60000000 ] || { echo "$f is over 60 MB; larger pushes fail through the session proxy. Re-encode it with a higher CRF."; exit 1; }
done
tmp="$(mktemp -d)"
git -C "$tmp" init -q -b "video/$name"
cp "$@" "$tmp/"
git -C "$tmp" add -A
git -C "$tmp" -c user.name="sony-alias" -c user.email="sony-alias@users.noreply.github.com" \
  commit -q -m "Video files for $name" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git -C "$tmp" push -q "$remote" "video/$name:video/$name"
rm -rf "$tmp"
for f in "$@"; do echo "https://github.com/$slug/blob/video/$name/$(basename "$f")"; done
