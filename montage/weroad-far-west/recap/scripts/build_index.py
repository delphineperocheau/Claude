"""Génère index.html du récap WeRoad Far West 360°."""
import json, html, subprocess, sys
from PIL import Image
sys.path.insert(0, 'scripts'); from shots import SHOTS, END_BG, END
M = {int(k): v for k, v in json.load(open('media/index.json')).items()}
logo = open('assets/weroad-logo.svg').read()
def logo_svg(cls, road):
    return logo.replace('<svg ', f'<svg class="{cls}" ', 1).replace('#4D4D4D', road)

el, js = [], []
t = 0.0
chapters = []  # (start, label)
for i, (k, d, lab) in enumerate(SHOTS):
    m = M[k]; s = round(t, 3); sid = f"s{i}"
    if lab: chapters.append((s, lab))
    zin = i % 2 == 0
    if m['kind'] == 'video':
        el.append(f'<video id="{sid}" class="clip shot" src="{m["file"]}" data-start="{s}" data-duration="{d}" data-media-start="0.3" data-track-index="0" muted playsinline></video>')
        js.append(f'tl.fromTo("#{sid}", {{scale: {1.0 if zin else 1.08}}}, {{scale: {1.08 if zin else 1.0}, duration: {d}, ease: "none"}}, {s});')
    else:
        w, h = Image.open(m['file']).size
        if m['land']:
            iw = round(w * 1920 / h); over = iw - 1080
            a, b = (-over * 0.15, -over * 0.75) if zin else (-over * 0.75, -over * 0.15)
            el.append(f'<div id="{sid}" class="clip scene" data-start="{s}" data-duration="{d}" data-track-index="0"><img id="{sid}-img" class="pan" src="{m["file"]}" alt="" style="width:{iw}px" /></div>')
            js.append(f'tl.fromTo("#{sid}-img", {{x: {a:.0f}}}, {{x: {b:.0f}, duration: {d}, ease: "none"}}, {s});')
        else:
            el.append(f'<div id="{sid}" class="clip scene" data-start="{s}" data-duration="{d}" data-track-index="0"><img id="{sid}-img" class="cover" src="{m["file"]}" alt="" /></div>')
            js.append(f'tl.fromTo("#{sid}-img", {{scale: {1.02 if zin else 1.12}}}, {{scale: {1.12 if zin else 1.02}, duration: {d}, ease: "none"}}, {s});')
    t += d
e0 = round(t, 3); total = round(e0 + END, 3)

# étiquettes de lieu (durée du chapitre) + balayage corail aux changements de chapitre
for j, (s, lab) in enumerate(chapters):
    en = chapters[j + 1][0] if j + 1 < len(chapters) else e0
    s2 = round(s + (3.15 if j == 0 else 0.15), 3); d = round(en - s2, 3)
    el.append(f'<div id="lab-{j}" class="clip lab" data-start="{s2}" data-duration="{d}" data-track-index="3"><span class="pin"></span><span class="lab-t">{html.escape(lab.upper())}</span></div>')
    js.append(f'tl.fromTo("#lab-{j}", {{xPercent: -120}}, {{xPercent: 0, duration: 0.45, ease: "power3.out"}}, {s2});')
    if j > 0:
        ws = round(s - 0.2, 3)
        el.append(f'<div id="wipe-{j}" class="clip wipe" data-start="{ws}" data-duration="0.5" data-track-index="4"></div>')
        js.append(f'tl.fromTo("#wipe-{j}", {{xPercent: -101}}, {{xPercent: 101, duration: 0.5, ease: "power2.inOut"}}, {ws});')

# logo permanent
el.append(f'<div id="wm" class="clip" data-start="0.4" data-duration="{round(e0 - 0.4, 3)}" data-track-index="5">{logo_svg("wm-svg", "#FFFFFF")}</div>')
js.append('tl.fromTo("#wm", {opacity: 0}, {opacity: 0.95, duration: 0.5}, 0.4);')

# intro
el.append('''<div id="intro" class="clip" data-start="0" data-duration="3.3" data-track-index="6" data-layout-allow-overlap>
  <div class="i-shade"></div>
  <div class="i-txt">
    <p id="i-kick"><span>Récap de voyage</span></p>
    <h1 id="i-t1" data-layout-allow-overlap>Far West</h1>
    <h1 id="i-t2" data-layout-allow-overlap>360°</h1>
    <p id="i-sub">Los Angeles · Las Vegas<span class="blk">et les grands parcs américains</span></p>
    <p id="i-date">22.03 → 02.04.2026</p>
  </div>
</div>''')
js += [
    'tl.fromTo("#i-kick span", {yPercent: 110}, {yPercent: 0, duration: 0.4, ease: "power3.out"}, 0.1);',
    'tl.fromTo("#i-t1", {y: 90, opacity: 0}, {y: 0, opacity: 1, duration: 0.5, ease: "power3.out"}, 0.25);',
    'tl.fromTo("#i-t2", {scale: 0.3, opacity: 0}, {scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)"}, 0.5);',
    'tl.fromTo("#i-sub", {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 0.4}, 0.85);',
    'tl.fromTo("#i-date", {y: 30, opacity: 0}, {y: 0, opacity: 1, duration: 0.4}, 1.05);',
    'tl.to("#intro .i-txt", {y: -60, opacity: 0, duration: 0.35, ease: "power2.in"}, 2.9);',
    'tl.to("#intro .i-shade", {opacity: 0, duration: 0.4}, 2.9);',
]

# fin
el.append(f'''<div id="end" class="clip scene" data-start="{e0}" data-duration="{END}" data-track-index="0" data-layout-allow-overlap>
  <img id="e-bg" class="cover" src="{M[END_BG]["file"]}" alt="" />
  <div class="e-shade"></div>
  <div class="e-txt">
    {logo_svg("e-logo", "#FFFFFF")}
    <div id="e-line"></div>
    <p id="e-t">Far West 360°</p>
    <p id="e-d">22.03 → 02.04.2026</p>
    <p id="e-m">Merci la team.</p>
  </div>
</div>''')
js += [
    f'tl.fromTo("#e-bg", {{scale: 1.15}}, {{scale: 1.02, duration: {END}, ease: "none"}}, {e0});',
    f'tl.fromTo("#end .e-logo", {{scale: 0.7, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.8)"}}, {e0 + 0.2});',
    f'tl.fromTo("#e-line", {{scaleX: 0}}, {{scaleX: 1, duration: 0.4, ease: "power3.out"}}, {e0 + 0.7});',
    f'tl.fromTo("#e-t", {{y: 40, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45}}, {e0 + 0.9});',
    f'tl.fromTo("#e-d", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45}}, {e0 + 1.1});',
    f'tl.fromTo("#e-m", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5}}, {e0 + 1.6});',
]

# audio
auto = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 0.5, "v": 1}, {"t": total - 1.2, "v": 1}, {"t": total, "v": 0}]}]}
el.append(f"<audio id=\"music\" src=\"assets/musique-pop.mp3\" data-start=\"0\" data-duration=\"{total}\" data-media-start=\"0\" data-track-index=\"11\" data-volume=\"0.9\" data-automation='{json.dumps(auto)}'></audio>")
def dur(f): return round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])), 3)
sfx = [("whoosh-cinematic", 0.0, 0.3)] + [("whoosh-short", round(s - 0.25, 3), 0.25) for s, _ in chapters[1:]] + [("chime", e0 + 0.2, 0.35)]
for i, (n, st, v) in enumerate(sfx):
    el.append(f'<audio id="sfx-{i}" src="assets/{n}.mp3" data-start="{max(0, st)}" data-duration="{dur("assets/" + n + ".mp3")}" data-track-index="{20 + i}" data-volume="{v}"></audio>')

page = f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Far West 360° WeRoad</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --coral: #FF4758; --ink: #171717; --cream: #FFF9EB; --white: #FFFFFF; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ink); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ink); font-family: Montserrat, sans-serif; }}
      .shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; background: var(--ink); }}
      .cover {{ position: absolute; inset: 0; display: block; width: 100%; height: 100%; object-fit: cover; }}
      .pan {{ position: absolute; top: 0; left: 0; display: block; height: 1920px; max-width: none; }}
      .lab {{ position: absolute; left: 0; bottom: 330px; display: flex; align-items: center; gap: 18px; background: var(--coral); color: var(--white); padding: 20px 38px 20px 60px; border-radius: 0 60px 60px 0; }}
      .pin {{ display: block; width: 26px; height: 26px; border-radius: 50%; border: 8px solid var(--white); }}
      .lab-t {{ font-weight: 900; font-size: 54px; letter-spacing: 0.02em; white-space: nowrap; }}
      .wipe {{ position: absolute; inset: 0; background: var(--coral); }}
      #wm {{ position: absolute; top: 110px; right: 60px; }}
      .wm-svg {{ display: block; width: 250px; height: auto; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.45)); }}
      #intro {{ position: absolute; inset: 0; }}
      .i-shade {{ position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(23,23,23,0.1) 20%, rgba(23,23,23,0.85) 75%); }}
      .i-txt {{ position: absolute; left: 80px; right: 80px; bottom: 330px; color: var(--white); }}
      #i-kick {{ overflow: hidden; margin-bottom: 20px; }}
      #i-kick span {{ display: inline-block; background: var(--coral); color: var(--white); font-weight: 900; font-size: 44px; text-transform: uppercase; padding: 8px 24px; border-radius: 12px; }}
      #i-t1, #i-t2 {{ font-weight: 900; font-size: 190px; line-height: 0.95; letter-spacing: -0.03em; text-transform: uppercase; }}
      #i-t2 {{ color: var(--coral); transform-origin: left center; }}
      #i-sub {{ margin-top: 30px; font-weight: 800; font-size: 50px; line-height: 1.2; }}
      .blk {{ display: block; font-weight: 600; font-size: 42px; }}
      #i-date {{ margin-top: 22px; font-weight: 700; font-size: 40px; color: var(--cream); }}
      .e-shade {{ position: absolute; inset: 0; background: rgba(23,23,23,0.62); }}
      .e-txt {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: var(--white); }}
      .e-logo {{ display: block; width: 720px; height: auto; }}
      #e-line {{ width: 220px; height: 12px; border-radius: 6px; background: var(--coral); margin: 70px 0 56px; }}
      #e-t {{ font-weight: 900; font-size: 110px; text-transform: uppercase; letter-spacing: -0.02em; white-space: nowrap; }}
      #e-d {{ margin-top: 18px; font-weight: 700; font-size: 50px; color: var(--cream); }}
      #e-m {{ margin-top: 80px; font-weight: 800; font-size: 60px; color: var(--white); }}
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
open('index.html', 'w').write(page)
print('total', total, 'chapitres', [(round(s, 1), l) for s, l in chapters])
