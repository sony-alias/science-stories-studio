"""Join narrated plates into one episode: 0.8 s crossfades, voice placed sample-exactly, YouTube loudness.

Usage:  python3 scripts/make_episode.py OUTPUT.mp4 PART1.mp4 PART2.mp4 [...]
All parts must be 1920x1080, 30 fps, with an audio track.
"""
import subprocess
import sys

F = 0.8  # crossfade length in seconds


def frames(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                                   "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path]).decode()
    return int(out.strip()) / 30.0


def main(out, files):
    d = [frames(f) for f in files]
    parts, mix_in, starts = [], [], [0.0]
    for i in range(len(files)):
        parts.append(f"[{i}:v]settb=AVTB,fps=30,format=yuv420p[v{i}]")
        parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=duration={d[i]:.4f}[a{i}]")
    vprev, acc = "v0", d[0]
    for i in range(1, len(files)):
        starts.append(acc - F)
        parts.append(f"[{vprev}][v{i}]xfade=transition=fade:duration={F}:offset={acc - F:.4f}[vx{i}]")
        vprev, acc = f"vx{i}", acc + d[i] - F
    for i in range(len(files)):
        ms = int(round(starts[i] * 1000))
        parts.append(f"[a{i}]afade=t=in:d={F / 2},afade=t=out:st={d[i] - F / 2:.4f}:d={F / 2},adelay={ms}|{ms}[ad{i}]")
        mix_in.append(f"[ad{i}]")
    parts.append("".join(mix_in) + f"amix=inputs={len(files)}:normalize=0:duration=longest,"
                 f"atrim=duration={acc:.4f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]")
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for f in files:
        cmd += ["-i", f]
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{vprev}]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.check_call(cmd)
    print(f"{out}: {acc:.2f} s from {len(files)} parts")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
