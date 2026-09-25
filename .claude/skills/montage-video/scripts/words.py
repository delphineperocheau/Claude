"""Affiche, pour chaque transcription, les mots horodatés et les silences détectés.
Les horodatages whisper sont souvent en retard de 0,5 à 1 s : caler les coupes sur les silences.
Usage : python3 words.py <dossier_travail>"""
import json, glob, subprocess, sys, re
W = sys.argv[1]
for f in sorted(glob.glob(f"{W}/*.json")):
    d = json.load(open(f))
    if "transcription" not in d: continue
    out = []
    for seg in d["transcription"]:
        for t in seg.get("tokens", []):
            if t["text"].startswith("[_"): continue
            out.append(f"{t['text']}@{t['offsets']['from']/1000:.1f}")
    print("==", f.split("/")[-1][:-5]); print("".join(out))
    wav = f[:-5] + ".wav"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "silencedetect=n=-35dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = re.findall(r"silence_start: ([\d.]+)", r); e = re.findall(r"silence_end: ([\d.]+)", r)
    print("  silences:", " ".join(f"[{a}-{b}]" for a, b in zip(s, e)))
