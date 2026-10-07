"""Génère index.html d'un rush « La météo du SEO » aux couleurs de poweb.
Usage : python3 scripts/build_index.py <id>   (depuis rushs/)"""
import html, json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from rushes import RUSHES, SEG_OFFSET

r = RUSHES[sys.argv[1]]
RID = r["id"]
D = round(sum(b - a for a, b in r["ranges"]), 3)
SPK = json.load(open(f"media/{RID}-speakers.json"))
NAMES = {"camille": "Camille Dufossez, École du SEO", "delphine": "Delphine Merlet, poweb"}
SHORT = {"camille": "Camille", "delphine": "Delphine"}
END = 3.4
total = round(D + END, 3)

# --- mots horodatés (whisper.cpp -ojf), relatifs au début du rush
words = []
for seg in json.load(open(f"media/{RID}-tr.json"))["transcription"]:
    for t in seg["tokens"]:
        tx = t["text"]
        if tx.startswith("[_") or not tx.strip():
            continue
        s = t["offsets"]["from"] / 1000
        if tx.startswith(" ") or not words:
            words.append([tx.strip(), s])
        else:
            words[-1][0] += tx
words = [w for w in words if w[0] and -0.2 <= w[1] < D - 0.1]
for w in words:
    w[1] = max(0.0, w[1])
# corrections de transcription (sur la suite de mots)
for old, new in r.get("fix", {}).items():
    ow, nw, i, hit = old.split(), new.split(), 0, False
    while i <= len(words) - len(ow):
        if [w[0] for w in words[i:i + len(ow)]] == ow:
            t0, t1 = words[i][1], words[i + len(ow) - 1][1]
            words[i:i + len(ow)] = [[x, t0 + (t1 - t0) * j / max(1, len(nw) - 1)] for j, x in enumerate(nw)]
            hit = True; i += len(nw)
        else:
            i += 1
    if not hit:
        print(f"ATTENTION correction introuvable : {old}", file=sys.stderr)
# blocs de 4 mots max, coupés aux ponctuations
chunks, cur = [], []
for w, st in words:
    cur.append((w, st))
    if w[-1] in ".?!" or w[-1] == "," and len(cur) >= 2 or len(cur) == 4:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    st = c[0][1]
    en = chunks[i + 1][0][1] if i + 1 < len(chunks) else min(D, c[-1][1] + 1.0)
    txt = " ".join(w for w, _ in c).strip(" ,")
    caps.append([round(st, 3), round(min(en, D), 3), txt])

def esc(s): return html.escape(s)

el, js = [], []
# webcams : la locutrice active en grand, l'autre dans le polaroïd
for k in ("camille", "delphine"):
    el.append(f'<video id="big-{k}" class="clip big" src="media/{RID}-{k}.mp4" data-start="0" data-duration="{D}" data-media-start="0" data-track-index="{0 if k == "camille" else 1}" muted playsinline></video>')
el.append(f'<div id="pola">'
          + "".join(f'<video id="sm-{k}" class="sm" src="media/{RID}-{k}-pola.mp4" data-start="0" data-duration="{D}" data-media-start="0" data-track-index="{2 if k == "camille" else 11}" muted playsinline></video>' for k in ("camille", "delphine"))
          + "".join(f'<span id="pn-{k}" class="pn">{SHORT[k]}</span>' for k in ("camille", "delphine")) + '</div>')
el.append(f'<audio id="voix" src="media/{RID}-voix.m4a" data-start="0" data-duration="{D}" data-media-start="0" data-track-index="10" data-volume="1"></audio>')
seen = set()
for j, (t, w) in enumerate(SPK):
    o = "delphine" if w == "camille" else "camille"
    js += [f'tl.set("#big-{w}, #sm-{o}, #pn-{o}", {{opacity: 1}}, {t});', f'tl.set("#big-{o}, #sm-{w}, #pn-{w}", {{opacity: 0}}, {t});']
    if t > 0:
        js.append(f'tl.fromTo("#pola", {{scale: 0.9}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {t});')
    if w not in seen and t < D - 3:
        seen.add(w)
        st = round(t + (0.8 if t == 0 else 0.1), 3)
        el.append(f'<div id="tag-{w}" class="clip etq noir tagname" data-start="{st}" data-duration="3.2" data-track-index="{4 if w == "camille" else 9}">{NAMES[w]}</div>')
        js.append(f'tl.fromTo("#tag-{w}", {{x: -80, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.35, ease: "power3.out"}}, {st});')
        js.append(f'tl.to("#tag-{w}", {{x: -80, opacity: 0, duration: 0.3, ease: "power2.in"}}, {round(st + 2.9, 3)});')
# étiquettes du haut
el.append(f'<div id="tag-meteo" class="clip etq blanc" data-start="0" data-duration="{D}" data-track-index="2">la météo du SEO ☀️</div>')
q_html = "".join(f'<span class="ql">{esc(l)}</span>' for l in r["question"])
el.append(f'<div id="tag-q" class="clip etq corail" data-start="0" data-duration="{D}" data-track-index="3">{q_html}</div>')
el.append(f'<div id="pied" class="clip" data-start="0" data-duration="{D}" data-track-index="5"><b>poweb</b><span>poweb85.fr</span></div>')
js += [
    'tl.fromTo("#tag-meteo", {scale: 0.6, opacity: 0, rotation: -9}, {scale: 1, opacity: 1, rotation: -3, duration: 0.35, ease: "back.out(2.2)"}, 0.05);',
    'tl.fromTo("#tag-q", {scale: 0.7, opacity: 0, rotation: 6}, {scale: 1, opacity: 1, rotation: 1.6, duration: 0.4, ease: "back.out(2)"}, 0.25);',
    'tl.fromTo("#pola", {y: -60, opacity: 0, rotation: 12}, {y: 0, opacity: 1, rotation: 5, duration: 0.45, ease: "back.out(1.8)"}, 0.5);',
    'tl.fromTo("#pied", {opacity: 0}, {opacity: 1, duration: 0.4}, 0.6);',
]
# sous-titres
for i, (st, en, txt) in enumerate(caps):
    d = round(max(0.25, en - st), 3)
    rot = (-1.4, 1.1, -0.6, 1.6)[i % 4]
    el.append(f'<div id="cap-{i}" class="clip cap" data-start="{st}" data-duration="{d}" data-track-index="6"><p class="cap-in" style="transform: rotate({rot}deg)">{esc(txt)}</p></div>')
    js.append(f'tl.fromTo("#cap-{i} .cap-in", {{scale: 0.92, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.14, ease: "power2.out"}}, {st});')
# fin
e0 = D
js.append(f'tl.set("#pola", {{opacity: 0}}, {e0});')
el.append(f'''<div id="end" class="clip" data-start="{e0}" data-duration="{END}" data-track-index="7" data-layout-allow-overlap>
  <p id="e-logo">poweb</p>
  <p id="e-l1" class="etq noir">Le replay en entier : lien en bio</p>
  <p id="e-l2" class="etq blanc">poweb85.fr</p>
</div>''')
js += [
    f'tl.fromTo("#e-logo", {{scale: 0.5, opacity: 0, rotation: -12}}, {{scale: 1, opacity: 1, rotation: -4, duration: 0.45, ease: "back.out(2)"}}, {e0 + 0.05});',
    f'tl.fromTo("#e-l1", {{x: 120, opacity: 0, rotation: 6}}, {{x: 0, opacity: 1, rotation: 2.5, duration: 0.35, ease: "back.out(2)"}}, {e0 + 0.45});',
    f'tl.fromTo("#e-l2", {{x: -120, opacity: 0, rotation: -6}}, {{x: 0, opacity: 1, rotation: -2, duration: 0.35, ease: "back.out(2)"}}, {e0 + 0.7});',
]
def dur(f): return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])), 3)
sfx = [("pop", 0.05, 0.35), ("pop", 0.25, 0.35), ("whoosh-short", e0 - 0.1, 0.45), ("pop", e0 + 0.45, 0.3), ("chime", e0 + 0.7, 0.3)]
for i, (n, st, v) in enumerate(sfx):
    el.append(f'<audio id="sfx-{i}" src="assets/{n}.mp3" data-start="{round(st, 3)}" data-duration="{dur("assets/" + n + ".mp3")}" data-track-index="{20 + i}" data-volume="{v}"></audio>')

page = f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>La météo du SEO, {esc(r["titre"])}</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Cabinet Grotesk"; src: url("assets/cabinet-500.woff2") format("woff2"); font-weight: 500; }}
      @font-face {{ font-family: "Cabinet Grotesk"; src: url("assets/cabinet-700.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "Cabinet Grotesk"; src: url("assets/cabinet-800.woff2") format("woff2"); font-weight: 800; }}
      :root {{ --noir: #14110E; --corail: #E97458; --blanc: #ffffff; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--noir); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--noir); font-family: "Cabinet Grotesk", sans-serif; }}
      .big {{ position: absolute; left: 0; top: 600px; width: 1080px; height: 822px; object-fit: cover; opacity: 0; }}
      #pola {{ position: absolute; left: 760px; top: 560px; width: 276px; padding: 12px 12px 0; background: var(--blanc); box-shadow: 0 10px 28px rgba(0,0,0,0.45); transform: rotate(5deg); }}
      #pola .sm {{ position: absolute; left: 12px; top: 12px; width: 252px; height: 192px; object-fit: cover; opacity: 0; }}
      #pola::before {{ content: ""; display: block; width: 252px; height: 192px; background: #2a2622; }}
      #pola .pn {{ position: absolute; left: 0; right: 0; top: 208px; font-weight: 700; font-size: 28px; color: var(--noir); text-align: center; opacity: 0; }}
      #pola::after {{ content: ""; display: block; height: 52px; }}
      .etq {{ position: absolute; display: inline-block; font-weight: 800; padding: 10px 24px 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.35); border-radius: 4px 9px 5px 8px; }}
      .etq.blanc {{ background: var(--blanc); color: var(--noir); }}
      .etq.noir {{ background: var(--noir); color: var(--blanc); border: 3px solid var(--blanc); }}
      .etq.corail {{ background: var(--corail); color: var(--noir); }}
      #tag-meteo {{ left: 80px; top: 270px; font-size: 40px; transform: rotate(-3deg); }}
      #tag-q {{ left: 72px; right: 90px; top: 350px; font-size: 64px; line-height: 1.06; padding: 18px 30px 22px; transform: rotate(1.6deg); }}
      #tag-q .ql {{ display: block; }}
      .tagname {{ left: 60px; top: 640px; font-size: 32px; font-weight: 700; transform: rotate(-2deg); }}
      .cap {{ position: absolute; left: 80px; right: 80px; top: 1290px; height: 220px; display: flex; align-items: flex-end; justify-content: center; }}
      .cap-in {{ background: var(--blanc); color: var(--noir); font-weight: 800; font-size: 60px; line-height: 1.12; text-align: center; padding: 12px 28px 16px; border-radius: 6px 10px 6px 12px; box-shadow: 0 8px 22px rgba(0,0,0,0.4); }}
      #pied {{ position: absolute; left: 0; right: 0; top: 1560px; display: flex; justify-content: center; align-items: baseline; gap: 22px; color: var(--blanc); }}
      #pied b {{ font-weight: 800; font-size: 44px; color: var(--corail); }}
      #pied span {{ font-weight: 500; font-size: 32px; }}
      #end {{ position: absolute; inset: 0; background: var(--corail); }}
      #e-logo {{ position: absolute; left: 0; right: 0; top: 640px; text-align: center; font-weight: 800; font-size: 250px; line-height: 1; color: var(--noir); transform: rotate(-4deg); }}
      #e-l1 {{ left: 100px; top: 980px; font-size: 54px; transform: rotate(2.5deg); }}
      #e-l2 {{ left: 330px; top: 1110px; font-size: 64px; transform: rotate(-2deg); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(el)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + x for x in js).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
if not os.environ.get("DRY"):
    open("index.html", "w").write(page)
print(RID, "total", total, "sous-titres", len(caps))
for c in caps: print(f"{c[0]:6.2f} {c[2]}")
