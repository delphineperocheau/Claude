"""Génère index.html du reel Carole Roig (Les Opticiens Mobiles)."""
import json, html, subprocess

TR = "/tmp/claude-0/-home-user-Claude/d5672aa2-0e42-53e5-9c68-c5116505d633/scratchpad/cr.json"
CUT_IN, VID_DUR = 2.25, 32.1
FIX = {"Carol": "Carole", "je vous allais obligatoirement": "vous allez obligatoirement", "qui déjà vous va": "qui vous va déjà"}
QUESTIONS = [(2.3, 7.6), (17.3, 19.4), (28.85, 32.6)]  # voix hors champ

# mots avec timings
words = []
for seg in json.load(open(TR))["transcription"]:
    for t in seg["tokens"]:
        tx = t["text"]
        if tx.startswith("[_"):
            continue
        s = t["offsets"]["from"] / 1000
        if tx.startswith(" ") or not words:
            words.append([tx.strip(), s])
        else:
            words[-1][0] += tx
words = [w for w in words if w[1] >= CUT_IN - 0.05]
merged = []
for w, st in words:
    if merged and w in ("?", "!", ".", ",", ":"):
        merged[-1][0] += " " + w if w in "?!:" else w
    else:
        merged.append([w, st])
words = merged
# regroupe : phrases (. ? !), puis découpage équilibré en blocs de 5 mots max
import math
sents, cur = [], []
for w, st in words:
    cur.append((w, st))
    if w[-1] in ".?!":
        sents.append(cur); cur = []
if cur: sents.append(cur)
chunks = []
for se in sents:
    n = math.ceil(len(se) / 5)
    size = math.ceil(len(se) / n)
    for k in range(0, len(se), size):
        chunks.append(se[k:k + size])
caps = []
for i, c in enumerate(chunks):
    st = c[0][1]
    en = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][1] + 0.8
    txt = " ".join(w for w, _ in c)
    q = any(a <= st < b for a, b in QUESTIONS)
    caps.append([st, en, txt, q])
full = " ".join(c[2] for c in caps)
for a, b in FIX.items():
    assert a in full or a == "qui déjà vous va", a
for c in caps:
    for a, b in {"Carol,": "Carole,", "je vous allais": "vous allez", "déjà vous va": "vous va déjà", "qui déjà vous": "qui vous", "Donc je vous": "Donc vous", "allais obligatoirement": "allez obligatoirement"}.items():
        c[2] = c[2].replace(a, b)

INTRO = 3.4
OUT_SCENES = [("photo1", "Partout", "où vous êtes"), ("photo2", "Bilans", "visuels"), ("photo3", "Conseils", "personnalisés")]
OUT_EACH = 2.1
END = 4.2
v0 = INTRO
o0 = v0 + VID_DUR
e0 = o0 + OUT_EACH * len(OUT_SCENES)
total = round(e0 + END, 3)

el, js = [], []
# --- intro
el.append(f'''<div id="intro" class="clip scene" data-start="0" data-duration="{INTRO}" data-track-index="1">
  <div class="kb"><img id="intro-img" src="media/photo2.jpg" alt="" /></div>
  <div class="shade"></div>
  <div class="intro-txt">
    <div class="glasses"><span class="o"></span><span class="bar"></span><span class="o"></span></div>
    <h1 id="i-name">Carole Roig</h1>
    <p id="i-job"><span>Opticien à domicile</span></p>
    <p id="i-where">en Vendée</p>
  </div>
</div>''')
js += [
    'tl.fromTo("#intro-img", {scale: 1.25}, {scale: 1.08, duration: 3.4, ease: "none"}, 0);',
    'tl.fromTo("#intro .glasses", {scale: 0, rotation: -30}, {scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2.5)"}, 0.15);',
    'tl.fromTo("#i-name", {y: 60, opacity: 0}, {y: 0, opacity: 1, duration: 0.5, ease: "power3.out"}, 0.4);',
    'tl.fromTo("#i-job span", {xPercent: -105}, {xPercent: 0, duration: 0.45, ease: "power3.out"}, 0.8);',
    'tl.fromTo("#i-where", {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 0.4, ease: "power2.out"}, 1.15);',
]
# --- vidéo
el.append(f'<video id="v-carole" class="clip shot" src="media/carole.mp4" data-start="{v0}" data-duration="{VID_DUR}" data-media-start="0" data-track-index="0" muted playsinline></video>')
el.append(f'<audio id="a-carole" src="media/carole.mp4" data-start="{v0}" data-duration="{VID_DUR}" data-media-start="0" data-track-index="10" data-volume="1"></audio>')
el.append(f'<div id="badge" class="clip" data-start="{v0}" data-duration="{VID_DUR}" data-track-index="4"><img src="media/logo.png" alt="Les Opticiens Mobiles" /></div>')
js.append(f'tl.fromTo("#badge img", {{y: -40, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4, ease: "power2.out"}}, {v0 + 0.2});')
for i, (st, en, txt, q) in enumerate(caps):
    s = round(v0 + st - CUT_IN, 3)
    d = round(max(0.3, en - st), 3)
    if s + d > o0:
        d = round(o0 - s, 3)
    cls = "cap q" if q else "cap"
    el.append(f'<div id="cap-{i}" class="clip {cls}" data-start="{s}" data-duration="{d}" data-track-index="3"><p class="cap-in">{html.escape(txt)}</p></div>')
    js.append(f'tl.fromTo("#cap-{i} .cap-in", {{y: 18, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.16, ease: "power2.out"}}, {s});')
# étiquette question / réponse
for j, (a, b) in enumerate(QUESTIONS):
    s = round(v0 + a - CUT_IN, 3); d = round(b - a, 3)
    el.append(f'<div id="qtag-{j}" class="clip qtag" data-start="{s}" data-duration="{d}" data-track-index="5">Question de cliente</div>')
    js.append(f'tl.fromTo("#qtag-{j}", {{x: -30, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.3}}, {s});')
# --- promesses
for k, (img, a, b) in enumerate(OUT_SCENES):
    s = round(o0 + k * OUT_EACH, 3)
    framed = img == "photo3"
    pic = f'<div class="frame"><img id="o-img-{k}" src="media/{img}.jpg" alt="" /></div>' if framed else f'<div class="kb"><img id="o-img-{k}" src="media/{img}.jpg" alt="" /></div><div class="shade"></div>'
    el.append(f'''<div id="out-{k}" class="clip scene{' dark' if framed else ''}" data-start="{s}" data-duration="{OUT_EACH}" data-track-index="1">
  {pic}
  <div class="promise"><span class="p1" id="p1-{k}">{html.escape(a)}</span><span class="p2" id="p2-{k}"><span>{html.escape(b)}</span></span></div>
</div>''')
    js += [
        f'tl.fromTo("#o-img-{k}", {{scale: 1.18}}, {{scale: 1.04, duration: {OUT_EACH}, ease: "none"}}, {s});',
        f'tl.fromTo("#p1-{k}", {{y: 80, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4, ease: "power3.out"}}, {s + 0.1});',
        f'tl.fromTo("#p2-{k} span", {{yPercent: 110}}, {{yPercent: 0, duration: 0.4, ease: "power3.out"}}, {s + 0.3});',
    ]
# --- fin
el.append(f'''<div id="end" class="clip scene light" data-start="{round(e0, 3)}" data-duration="{END}" data-track-index="1">
  <img id="e-logo" src="media/logo.png" alt="Les Opticiens Mobiles" />
  <div id="e-line"></div>
  <p id="e-name">Carole Roig</p>
  <p id="e-job">Opticien à domicile en Vendée</p>
  <p id="e-list"><span>Bilans visuels</span><span class="sep"></span><span>Conseils personnalisés</span></p>
</div>''')
js += [
    f'tl.fromTo("#e-logo", {{scale: 0.8, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.8)"}}, {e0 + 0.1});',
    f'tl.fromTo("#e-line", {{scaleX: 0}}, {{scaleX: 1, duration: 0.4, ease: "power3.out"}}, {e0 + 0.5});',
    f'tl.fromTo("#e-name", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4}}, {e0 + 0.7});',
    f'tl.fromTo("#e-job", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4}}, {e0 + 0.9});',
    f'tl.fromTo("#e-list", {{opacity: 0}}, {{opacity: 1, duration: 0.5}}, {e0 + 1.3});',
]
# --- audio
auto = {"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0}, {"t": 0.6, "v": 0.8}, {"t": v0 - 0.2, "v": 0.8}, {"t": v0 + 0.4, "v": 0.12},
    {"t": o0 - 0.3, "v": 0.12}, {"t": o0 + 0.2, "v": 0.8}, {"t": total - 1.2, "v": 0.8}, {"t": total, "v": 0}]}]}
el.append(f"<audio id=\"music\" src=\"assets/musique-douce.mp3\" data-start=\"0\" data-duration=\"{total}\" data-media-start=\"0\" data-track-index=\"11\" data-volume=\"0.7\" data-automation='{json.dumps(auto)}'></audio>")
def dur(f): return round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f])),3)
sfx = [("whoosh-cinematic", 0.0, 0.35), ("pop", 0.15, 0.4), ("whoosh-short", v0 - 0.15, 0.5)] + \
      [("whoosh-short", o0 + k * OUT_EACH - 0.12, 0.45) for k in range(len(OUT_SCENES))] + [("chime", e0 + 0.1, 0.4)]
for i, (n, st, v) in enumerate(sfx):
    el.append(f'<audio id="sfx-{i}" src="assets/{n}.mp3" data-start="{max(0, round(st, 3))}" data-duration="{dur("assets/"+n+".mp3")}" data-track-index="{20 + i}" data-volume="{v}"></audio>')

page = f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Carole Roig, opticien à domicile</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --char: #212121; --orange: #FB7828; --white: #ffffff; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--char); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--char); font-family: Montserrat, sans-serif; }}
      .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; background: var(--char); }}
      .scene.light {{ background: var(--white); }}
      .kb {{ position: absolute; inset: 0; overflow: hidden; }}
      .kb img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
      .shade {{ position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(33,33,33,0.15) 30%, rgba(33,33,33,0.88) 78%); }}
      .intro-txt {{ position: absolute; left: 80px; right: 80px; bottom: 360px; color: var(--white); }}
      .glasses {{ display: flex; align-items: center; margin-bottom: 36px; }}
      .glasses .o {{ display: block; width: 96px; height: 96px; border: 18px solid var(--orange); border-radius: 50%; }}
      .glasses .bar {{ display: block; width: 34px; height: 16px; background: var(--orange); }}
      #i-name {{ font-weight: 900; font-size: 128px; line-height: 1; letter-spacing: -0.02em; }}
      #i-job {{ margin-top: 26px; overflow: hidden; }}
      #i-job span {{ display: inline-block; background: var(--orange); color: var(--char); font-weight: 800; font-size: 62px; padding: 8px 26px; }}
      #i-where {{ margin-top: 18px; font-weight: 700; font-size: 62px; }}
      #badge {{ position: absolute; top: 110px; left: 60px; background: rgba(255,255,255,0.92); padding: 18px 26px; border-radius: 18px; }}
      #badge img {{ display: block; width: 300px; height: auto; }}
      .cap {{ position: absolute; left: 70px; right: 70px; bottom: 330px; display: flex; justify-content: center; }}
      .cap-in {{ background: var(--char); color: var(--white); font-weight: 800; font-size: 58px; line-height: 1.18; text-align: center; padding: 16px 30px; border-radius: 16px; border-bottom: 8px solid var(--orange); }}
      .cap.q .cap-in {{ background: var(--orange); color: var(--char); border-bottom-color: var(--char); font-style: italic; }}
      .qtag {{ position: absolute; left: 70px; bottom: 560px; background: var(--white); color: var(--char); font-weight: 800; font-size: 32px; letter-spacing: 0.08em; text-transform: uppercase; padding: 10px 20px; border-radius: 10px; }}
      .frame {{ position: absolute; left: 110px; top: 330px; width: 860px; height: 860px; overflow: hidden; border-radius: 28px; border: 10px solid var(--orange); }}
      .frame img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
      .promise {{ position: absolute; left: 80px; right: 80px; bottom: 360px; color: var(--white); }}
      .p1 {{ display: block; font-weight: 900; font-size: 140px; line-height: 1; letter-spacing: -0.02em; }}
      .p2 {{ display: block; overflow: hidden; margin-top: 12px; }}
      .p2 span {{ display: inline-block; font-weight: 800; font-size: 76px; color: var(--orange); }}
      #end {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: var(--char); }}
      #e-logo {{ display: block; width: 820px; height: auto; }}
      #e-line {{ width: 240px; height: 10px; background: var(--orange); margin: 70px 0 60px; }}
      #e-name {{ font-weight: 900; font-size: 96px; }}
      #e-job {{ margin-top: 14px; font-weight: 700; font-size: 50px; color: var(--char); }}
      #e-list {{ margin-top: 60px; display: flex; align-items: center; gap: 26px; font-weight: 700; font-size: 40px; color: var(--char); }}
      #e-list .sep {{ display: block; width: 18px; height: 18px; border-radius: 50%; background: var(--orange); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(el)}
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
print("total", total)
for c in caps: print(f"{c[0]:.2f} {'Q' if c[3] else ' '} {c[2]}")
