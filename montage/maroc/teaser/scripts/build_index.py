"""Génère index.html du teaser à partir de media/durations.json."""
import json, html

D = json.load(open("media/durations.json"))

# (clip id, type, sous-titre, mots surlignés, texte overlay)
SEQ = [
    ("broll-ballons", "hook", None, None, "Ils pensaient partir en vacances…"),
    ("broll-chameaux", "hook", None, None, None),
    ("broll-souk", "hook", None, None, "…mais chacun cache un secret."),
    ("broll-dunes", "hook", None, None, None),
    ("broll-feu-titre", "title", None, None, None),
    ("c01-audrey", "conf", "Je pense qu'Audrey est propriétaire de bar.", ["propriétaire de bar"], None),
    ("c02-delphine", "conf", "Je pense que Delphine t'es propriétaire de… Ah oui ? Toi aussi ?", ["Toi aussi ?"], None),
    ("c03-pierre", "conf", "Pierre a eu un petit accident de voiture au Mexique.", ["accident de voiture"], None),
    ("c04-diana", "conf", "Je pense que Diana a été aux 24h du Mans.", ["24h du Mans"], None),
    ("c05-dino", "conf", "Dino a déjà fait des fouilles archéologiques.", ["fouilles archéologiques"], None),
    ("c06-sebastien", "conf", "Je pense que Sébastien a besoin de deux doses d'anesthésie.", ["deux doses d'anesthésie"], None),
    ("broll-the", "break", None, None, None),
    ("broll-feu", "break", None, None, "Et puis…"),
    ("c07-marion", "conf", "Alors moi je pense… c'est Marion, qui est pupille de l'État et née sous X.", ["née sous X"], None),
    ("c08-sousx", "conf", "La personne c'est sous X… je ne peux pas l'entendre ça. C'est trop dur pour moi.", ["trop dur pour moi"], None),
    ("c09-bivouac", "conf", "La personne qui est tombée dans un feu lors d'un bivouac…", ["tombée dans un feu"], None),
    ("c10-bestiole", "conf", "Dégueulasse ! Je croyais qu'il y avait pas de bestiole ici !", ["Dégueulasse !"], None),
    ("c11-coeur", "conf", "Parce que j'ai le cœur riche.", ["cœur riche"], None),
    ("c12-jeanpaul-a", "conf", "Donc je dis que c'est Jean-Paul.", ["Jean-Paul"], None),
    ("c13-jeanpaul-b", "conf", "Pour moi, c'est Jean-Paul.", ["Jean-Paul"], None),
]
END = 4.5

t = 0.0
items = []
for sid, kind, cap, hl, over in SEQ:
    d = D[sid]
    if kind == "title":
        d = 3.2
    items.append(dict(id=sid, kind=kind, start=round(t, 3), dur=round(d, 3), cap=cap, hl=hl or [], over=over))
    t += d
end_start = round(t, 3)
total = round(t + END, 3)

def caption_html(cap, hl):
    s = html.escape(cap)
    for h in hl:
        s = s.replace(html.escape(h), f'<span class="hl">{html.escape(h)}</span>')
    return s

vid, aud, ovl, js = [], [], [], []
music_pts = [{"t": 0, "v": 0.0}, {"t": 0.8, "v": 0.9}]
sfx = []
for i, it in enumerate(items):
    s, d, sid = it["start"], it["dur"], it["id"]
    vid.append(f'<video id="v-{sid}" class="clip shot" src="media/{sid}.mp4" data-start="{s}" data-duration="{d}" data-media-start="0" data-track-index="0" muted playsinline></video>')
    vol = "1" if it["kind"] == "conf" else "0.35"
    aud.append(f'<audio id="a-{sid}" src="media/{sid}.mp4" data-start="{s}" data-duration="{d}" data-media-start="0" data-track-index="10" data-volume="{vol}"></audio>')
    if it["kind"] == "conf":
        ovl.append(f'<div id="cap-{sid}" class="clip cap" data-start="{s}" data-duration="{d}" data-track-index="3"><p class="cap-in">{caption_html(it["cap"], it["hl"])}</p></div>')
        js.append(f'tl.fromTo("#cap-{sid} .cap-in", {{opacity: 0, y: 30, scale: 0.94}}, {{opacity: 1, y: 0, scale: 1, duration: 0.22, ease: "back.out(2)"}}, {s + 0.05});')
        js.append(f'tl.fromTo("#v-{sid}", {{scale: 1.0}}, {{scale: 1.06, duration: {d}, ease: "none"}}, {s});')
        # flash blanc sur chaque coupe
        js.append(f'tl.set("#flash", {{opacity: 0.55}}, {s}).to("#flash", {{opacity: 0, duration: 0.14}}, {s});')
        sfx.append(("whoosh-short", s - 0.12, 0.45))
    if it["over"]:
        ovl.append(f'<div id="ov-{sid}" class="clip over" data-start="{s}" data-duration="{d}" data-track-index="4"><p class="over-in">{html.escape(it["over"])}</p></div>')
        js.append(f'tl.fromTo("#ov-{sid} .over-in", {{opacity: 0, scale: 1.15}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "power2.out"}}, {s + 0.1});')
    if it["kind"] in ("hook", "break"):
        js.append(f'tl.fromTo("#v-{sid}", {{scale: 1.12}}, {{scale: 1.0, duration: {d}, ease: "power1.out"}}, {s});')
    # musique : forte sur b-roll/titre, baissée sous les voix
    level = {"conf": 0.22, "hook": 0.9, "title": 1.0, "break": 0.8}[it["kind"]]
    if sid == "c07-marion":
        level = 0.08  # tension : quasi silence
    music_pts.append({"t": round(s + 0.05, 3), "v": level})
    music_pts.append({"t": round(s + d - 0.05, 3), "v": level})

title = next(x for x in items if x["kind"] == "title")
marion = next(x for x in items if x["id"] == "c07-marion")
jp = next(x for x in items if x["id"] == "c12-jeanpaul-a")
sfx += [
    ("riser", title["start"] - 2.6, 0.7),
    ("impact-bass-1", title["start"], 1.0),
    ("glitch-1", title["start"] + 0.9, 0.5),
    ("whoosh-cinematic", marion["start"] - 1.2, 0.8),
    ("impact-bass-2", marion["start"], 0.8),
    ("riser", jp["start"] - 2.8, 0.5),
    ("impact-bass-1", end_start, 1.0),
    ("impact-bass-2", end_start + 1.6, 0.9),
]
music_pts += [{"t": end_start, "v": 1.0}, {"t": total - 1.2, "v": 0.9}, {"t": total, "v": 0.0}]
music_pts.sort(key=lambda p: p["t"])
auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": music_pts}]})

import subprocess
SFXD = {n: round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"assets/{n}.mp3"])), 3) for n in set(x[0] for x in sfx)}
sfx_html = []
for i, (name, st, v) in enumerate(sfx):
    sfx_html.append(f'<audio id="sfx-{i}" src="assets/{name}.mp3" data-start="{max(0, round(st, 3))}" data-duration="{SFXD[name]}" data-track-index="{20 + i}" data-volume="{v}"></audio>')

# confessionnal tag + titre + fin
ts, te = title["start"], end_start
js.append(f'tl.fromTo("#t-maroc", {{scale: 2.2, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.35, ease: "expo.out"}}, {ts});')
js.append(f'tl.fromTo("#t-band", {{scaleX: 0}}, {{scaleX: 1, duration: 0.4, ease: "power3.out"}}, {ts + 0.45});')
js.append(f'tl.fromTo("#t-rev", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.3}}, {ts + 0.7});')
js.append(f'tl.to("#t-maroc", {{x: 8, duration: 0.05, repeat: 5, yoyo: true, ease: "none"}}, {ts + 0.9});')
js.append(f'tl.set("#flash", {{opacity: 1}}, {ts}).to("#flash", {{opacity: 0, duration: 0.3}}, {ts});')
js.append(f'tl.fromTo("#e-q", {{opacity: 0, scale: 1.3}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "expo.out"}}, {te + 0.1});')
js.append(f'tl.to("#e-q", {{opacity: 0, duration: 0.25}}, {te + 1.45});')
js.append(f'tl.fromTo("#e-title", {{opacity: 0, scale: 1.4}}, {{opacity: 1, scale: 1, duration: 0.4, ease: "expo.out"}}, {te + 1.6});')
js.append(f'tl.fromTo("#e-suite", {{opacity: 0}}, {{opacity: 1, duration: 0.5}}, {te + 2.4});')
js.append(f'tl.set("#flash", {{opacity: 0.9}}, {te + 1.6}).to("#flash", {{opacity: 0, duration: 0.25}}, {te + 1.6});')
conf_windows = []
for it in items:
    if it["kind"] == "conf":
        if conf_windows and abs(conf_windows[-1][1] - it["start"]) < 0.01:
            conf_windows[-1][1] = it["start"] + it["dur"]
        else:
            conf_windows.append([it["start"], it["start"] + it["dur"]])
for i, (a, b) in enumerate(conf_windows):
    ovl.append(f'<div id="tag-{i}" class="clip tag" data-start="{round(a, 3)}" data-duration="{round(b - a, 3)}" data-track-index="5"><span class="dot"></span>CONFESSION</div>')
    js.append(f'tl.fromTo("#tag-{i} .dot", {{opacity: 1}}, {{opacity: 0.15, duration: 0.5, repeat: {int((b - a) / 0.5)}, yoyo: true, ease: "none"}}, {round(a, 3)});')

page = f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Maroc, les révélations</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; font-family: Montserrat, sans-serif; }}
      .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .vignette {{ position: absolute; inset: 0; pointer-events: none;
        background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%),
                    linear-gradient(to bottom, rgba(0,0,0,0) 62%, rgba(0,0,0,0.7) 100%); }}
      .cap {{ position: absolute; left: 70px; right: 70px; bottom: 300px; display: flex; justify-content: center; }}
      .cap-in {{ font-weight: 900; font-size: 62px; line-height: 1.12; color: #fff; text-align: center;
        text-transform: uppercase; letter-spacing: -0.01em;
        text-shadow: 0 4px 0 #000, 0 0 18px rgba(0,0,0,0.9); -webkit-text-stroke: 3px #000; paint-order: stroke fill; }}
      .hl {{ color: #FFD60A; white-space: nowrap; }}
      .over {{ position: absolute; left: 60px; right: 60px; top: 0; bottom: 0; display: flex; align-items: center; justify-content: center; }}
      .over-in {{ font-family: "League Gothic", sans-serif; font-size: 138px; line-height: 1; color: #fff; text-align: center;
        text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,0.85); }}
      .tag {{ position: absolute; top: 120px; left: 70px; display: flex; align-items: center; gap: 18px;
        font-weight: 800; font-size: 34px; letter-spacing: 0.22em; color: #fff; background: rgba(0,0,0,0.55);
        padding: 14px 26px; border-left: 8px solid #E10600; }}
      .dot {{ display: block; width: 22px; height: 22px; border-radius: 50%; background: #E10600; }}
      #title {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #t-maroc {{ font-family: "League Gothic", sans-serif; font-size: 400px; line-height: 0.9; color: #FFD60A;
        text-shadow: 0 10px 50px rgba(0,0,0,0.9); letter-spacing: 0.02em; }}
      #t-band {{ margin-top: 10px; background: #E10600; padding: 12px 40px; transform-origin: left center; }}
      #t-rev {{ display: block; font-weight: 900; font-size: 84px; color: #fff; letter-spacing: 0.04em; text-transform: uppercase; }}
      #end {{ position: absolute; inset: 0; background: #000; display: flex; align-items: center; justify-content: center; }}
      #e-q .l {{ display: block; }}
      #e-q {{ position: absolute; font-family: "League Gothic", sans-serif; font-size: 190px; color: #fff; text-align: center; line-height: 0.95; }}
      #e-title {{ display: flex; flex-direction: column; align-items: center; }}
      #e-title .m {{ font-family: "League Gothic", sans-serif; font-size: 300px; line-height: 0.9; color: #FFD60A; }}
      #e-title .r {{ margin-top: 10px; background: #E10600; padding: 10px 34px; font-weight: 900; font-size: 70px; color: #fff; letter-spacing: 0.04em; }}
      #e-suite {{ position: absolute; bottom: 380px; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 44px; letter-spacing: 0.4em; color: #fff; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      {chr(10).join("      " + x for x in vid).strip()}
      <div class="vignette"></div>
      <div id="title" class="clip" data-start="{ts}" data-duration="{title['dur']}" data-track-index="6">
        <div id="t-maroc">MAROC</div>
        <div id="t-band"><span id="t-rev">Les révélations</span></div>
      </div>
      {chr(10).join("      " + x for x in ovl).strip()}
      <div id="end" class="clip" data-start="{te}" data-duration="{END}" data-track-index="7">
        <div id="e-q" data-layout-allow-overlap><span class="l">QUI CACHE</span><span class="l">QUOI ?</span></div>
        <div id="e-title" data-layout-allow-overlap><div class="m">MAROC</div><div class="r">LES RÉVÉLATIONS</div></div>
        <div id="e-suite">À SUIVRE…</div>
      </div>
      <div id="flash"></div>
      {chr(10).join("      " + x for x in aud).strip()}
      <audio id="music" src="assets/musique-suspense.mp3" data-start="0" data-duration="{total}" data-media-start="0" data-track-index="11" data-volume="0.8" data-automation='{auto}'></audio>
      {chr(10).join("      " + x for x in sfx_html).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in js).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open("index.html", "w").write(page)
print("total", total, "end_start", end_start)
