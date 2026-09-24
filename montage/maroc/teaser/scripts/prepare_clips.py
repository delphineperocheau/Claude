"""Découpe et normalise les rushes du teaser (1080x1920, 30 fps, étalonnage, son normalisé).
Usage : python3 scripts/prepare_clips.py  (depuis montage/maroc/teaser, rushes dans ../rushes)"""
import subprocess, os, json

R = "../rushes/"
OUT = "media/"
# id, fichier, [(in, out), ...], type
SEGMENTS = [
    ("broll-ballons", "VID20250918071135", [(3.0, 5.4)], "broll"),
    ("broll-chameaux", "VID20250919191236", [(3.0, 5.2)], "broll"),
    ("broll-souk", "VID20250924204030", [(4.0, 6.0)], "broll"),
    ("broll-dunes", "VID20250920072736", [(12.0, 14.2)], "broll"),
    ("broll-feu-titre", "VID20250919220022", [(5.0, 9.0)], "landscape"),
    ("c01-audrey", "VID20250919223435", [(0.8, 3.2)], "conf"),
    ("c02-delphine", "VID20250919224344", [(0.0, 4.4)], "conf"),
    ("c03-pierre", "VID20250919223604", [(2.5, 6.0)], "conf"),
    ("c04-diana", "VID20250919223325", [(0.9, 4.7)], "conf"),
    ("c05-dino", "VID20250919223812", [(8.0, 13.1)], "conf"),
    ("c06-sebastien", "VID20250919223652", [(3.6, 4.3), (5.5, 11.95)], "conf"),
    ("broll-the", "VID20250918152644", [(5.0, 6.8)], "broll"),
    ("broll-feu", "VID20250919220022", [(15.0, 16.8)], "landscape"),
    ("c07-marion", "Diana", [(1.15, 2.55), (3.3, 10.9)], "conf"),
    ("c08-sousx", "VID20250919224218", [(13.3, 17.8)], "conf"),
    ("c09-bivouac", "VID20250919223932", [(0.2, 4.15)], "conf"),
    ("c10-bestiole", "VID20250919223932", [(7.9, 12.3)], "conf"),
    ("c11-coeur", "VID20250919224151", [(11.5, 15.0)], "conf"),
    ("c12-jeanpaul-a", "VID20250919224218", [(18.25, 19.85)], "conf"),
    ("c13-jeanpaul-b", "VID20250919223932", [(15.2, 16.95)], "conf"),
]

GRADE = {
    "conf": "eq=brightness=0.05:contrast=1.15:saturation=1.1:gamma=1.08,colorbalance=bs=0.04:bm=0.02:bh=-0.03,unsharp=5:5:0.5",
    "broll": "eq=contrast=1.08:saturation=1.18",
    "landscape": "eq=contrast=1.08:saturation=1.18",
}

def run(cmd):
    subprocess.run(cmd, check=True)

os.makedirs(OUT, exist_ok=True)
durations = {}
for sid, src, ranges, kind in SEGMENTS:
    parts = []
    for i, (a, b) in enumerate(ranges):
        p = f"{OUT}_{sid}_{i}.mp4"
        if kind == "landscape":
            vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.15[bg];"
                  f"[b]scale=1080:-2,{GRADE[kind]}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]")
        else:
            vf = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{GRADE[kind]},fps=30,format=yuv420p[v]"
        af = "loudnorm=I=-16:TP=-1.5,aresample=48000" if kind == "conf" else "volume=0.6,aresample=48000"
        run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-t", f"{b - a:.3f}", "-i", R + src + ".mp4",
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
        for x in parts + [lst]:
            os.remove(x)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]))
    durations[sid] = round(d, 3)
    print(sid, durations[sid], flush=True)
json.dump(durations, open(OUT + "durations.json", "w"), indent=1)
