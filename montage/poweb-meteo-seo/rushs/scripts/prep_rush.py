"""Prépare les médias d'un rush : webcams de Camille et de Delphine (1080x932), voix normalisée,
locutrice active (mouvement des webcams) et transcription fine (whisper small + DTW).
Usage : python3 scripts/prep_rush.py <id>   (depuis rushs/)"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from rushes import RUSHES, SEG_OFFSET

SRC = "../rushes/meteo-seo-mars-2025.mp4"
# Disposition Restream « caméras » (source 1280x720) : Camille en haut à gauche, Delphine en dessous.
CROP = {"camille": "415:316:0:0", "delphine": "415:316:0:363"}  # sans les étiquettes de nom Restream
GRADE = "eq=brightness=0.03:contrast=1.06:saturation=1.08,unsharp=5:5:0.6"
WH = "/root/.cache/hyperframes/whisper"
PROMPT = "Webinaire La météo du SEO avec Camille Dufossez de l'École du SEO et Delphine de poweb. FAQ, SERP, Semrush, mots-clés, backlinks."

def run(cmd): subprocess.run(cmd, check=True)

r = RUSHES[sys.argv[1]]
RID, off = r["id"], SEG_OFFSET[r["seg"]]
os.makedirs("media", exist_ok=True)
tmp = f"media/_{RID}"
os.makedirs(tmp, exist_ok=True)
parts = {"camille": [], "delphine": [], "voix": []}
motion = []
for i, (a, b) in enumerate(r["ranges"]):
    s, d = off + a, b - a
    fc = ";".join([f"[0:v]split[c][d]"] +
                  [f"[{k[0]}]crop={CROP[k]},scale=1080:822:flags=lanczos,{GRADE},fps=30,format=yuv420p[v{k[0]}]" for k in CROP] +
                  ["[0:a]highpass=f=80,aresample=48000[au]"])
    run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-filter_complex", fc,
         "-map", "[vc]", "-an", "-c:v", "libx264", "-crf", "18", f"{tmp}/c{i}.mp4",
         "-map", "[vd]", "-an", "-c:v", "libx264", "-crf", "18", f"{tmp}/d{i}.mp4",
         "-map", "[au]", "-vn", "-c:a", "pcm_s16le", "-ac", "1", f"{tmp}/a{i}.wav"])
    parts["camille"].append(f"c{i}.mp4"); parts["delphine"].append(f"d{i}.mp4"); parts["voix"].append(f"a{i}.wav")
    # mouvement des visages, fenêtres de 0,5 s
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-vf",
                          "fps=10,crop=415:720:0:0,scale=160:280,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 280, 160).astype(np.float32)
    dc = np.abs(np.diff(f[:, 50:125, 40:120], axis=0)).mean((1, 2))
    dd = np.abs(np.diff(f[:, 200:270, 40:120], axis=0)).mean((1, 2))
    for k in range(len(dc) // 5):
        motion.append((dc[k * 5:(k + 1) * 5].mean(), dd[k * 5:(k + 1) * 5].mean()))
for k, lst in parts.items():
    open(f"{tmp}/{k}.txt", "w").write("".join(f"file '{x}'\n" for x in lst))
for k in ("camille", "delphine"):
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/{k}.txt", "-c", "copy", f"media/{RID}-{k}.mp4"])
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"media/{RID}-{k}.mp4", "-vf", "scale=504:384", "-c:v", "libx264", "-crf", "20", f"media/{RID}-{k}-pola.mp4"])
run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/voix.txt",
     "-af", "loudnorm=I=-16:TP=-1.5,aresample=48000", "-c:a", "aac", "-b:a", "192k", "-ac", "2", f"media/{RID}-voix.m4a"])

# locutrice active : moyenne glissante sur 2 s, hystérésis, plans de 1,5 s minimum
m = np.array(motion)
k = 4
sm = np.array([m[max(0, i - k):i + k + 1].mean(0) for i in range(len(m))])
who, cur = [], r.get("first", "camille")
for c, d in sm:
    if cur == "camille" and d > c * 1.35: cur = "delphine"
    elif cur == "delphine" and c > d * 1.35: cur = "camille"
    who.append(cur)
spk = []
for i, w in enumerate(who):
    t = i * 0.5
    if not spk or spk[-1][1] != w:
        if spk and t - spk[-1][0] < 1.5:
            spk[-1][1] = w
            if len(spk) > 1 and spk[-2][1] == w: spk.pop()
        else:
            spk.append([t, w])
for t, w in r.get("force", []):
    spk = [x for x in spk if abs(x[0] - t) > 0.01]
    spk.append([t, w])
spk.sort()
if "speakers" in r:  # plans imposés après vérification à l'image
    spk = [list(x) for x in r["speakers"]]
json.dump(spk, open(f"media/{RID}-speakers.json", "w"))

# transcription fine du rush
wav16 = f"{tmp}/voix16.wav"
run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/voix.txt", "-ar", "16000", "-ac", "1", wav16])
subprocess.run([f"{WH}/whisper.cpp/build/bin/whisper-cli", "-m", f"{WH}/models/ggml-small.bin", "--dtw", "small", "-l", "fr",
                "-t", str(os.cpu_count()), "--prompt", PROMPT, "-ojf", "-of", f"media/{RID}-tr", wav16],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("ok", RID, round(sum(b - a for a, b in r["ranges"]), 2), "plans", [(round(t, 1), w[0]) for t, w in spk])
