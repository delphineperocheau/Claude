"""Découpe et normalise des segments vidéo pour HyperFrames.
Sortie : <out>/<id>.mp4 (1080x1920 ou 1920x1080, 30 fps, H.264, étalonnage, son normalisé) + durations.json
Usage : python3 prepare_clips.py segments.json
segments.json :
{
  "rushes": "../rushes/", "out": "media/", "format": "portrait",   # portrait | landscape
  "segments": [
    {"id": "c01-intro", "src": "VID123.mp4", "ranges": [[0.8, 3.2]], "kind": "parole"},
    {"id": "broll-dunes", "src": "VID456.mp4", "ranges": [[12, 14.2]], "kind": "broll"}
  ]
}
kind : parole (son normalisé -16 LUFS, étalonnage éclaircissant) | broll (son d'ambiance à 60 %)
Une source d'orientation différente du format est posée sur un fond flouté (pas de recadrage)."""
import subprocess, os, json, sys

cfg = json.load(open(sys.argv[1]))
R, OUT = cfg["rushes"], cfg["out"]
W, H = (1080, 1920) if cfg.get("format", "portrait") == "portrait" else (1920, 1080)
GRADE = {
    "parole": cfg.get("grade_parole", "eq=brightness=0.04:contrast=1.1:saturation=1.08:gamma=1.05,unsharp=5:5:0.4"),
    "broll": cfg.get("grade_broll", "eq=contrast=1.08:saturation=1.15"),
}

def run(cmd): subprocess.run(cmd, check=True)
def probe_wh(path):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height:stream_side_data=rotation", "-of", "json", path])
    s = json.loads(o)["streams"][0]; w, h = s["width"], s["height"]
    rot = next((abs(int(x.get("rotation", 0))) for x in s.get("side_data_list", []) if "rotation" in x), 0)
    return (h, w) if rot in (90, 270) else (w, h)

os.makedirs(OUT, exist_ok=True)
durations = {}
for seg in cfg["segments"]:
    sid, src, kind = seg["id"], R + seg["src"], seg.get("kind", "parole")
    w, h = probe_wh(src)
    fits = (w >= h) == (W >= H)
    parts = []
    for i, (a, b) in enumerate(seg["ranges"]):
        p = f"{OUT}_{sid}_{i}.mp4"
        g = GRADE[kind]
        if fits:
            vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{g},fps=30,format=yuv420p[v]"
        else:
            vf = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2,eq=brightness=-0.15[bg];"
                  f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease,{g}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]")
        af = "highpass=f=80,loudnorm=I=-16:TP=-1.5,aresample=48000" if kind == "parole" else "volume=0.6,aresample=48000"
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-t", f"{b - a:.3f}", "-i", src,
             "-filter_complex", vf + f";[0:a]{af}[au]", "-map", "[v]", "-map", "[au]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-ac", "2", p])
        parts.append(p)
    final = f"{OUT}{sid}.mp4"
    if len(parts) == 1:
        os.replace(parts[0], final)
    else:
        lst = f"{OUT}_{sid}.txt"
        open(lst, "w").write("".join(f"file '{os.path.basename(x)}'\n" for x in parts))
        run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", final])
        for x in parts + [lst]: os.remove(x)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]))
    durations[sid] = round(d, 3)
    print(sid, durations[sid], flush=True)
json.dump(durations, open(OUT + "durations.json", "w"), indent=1)
