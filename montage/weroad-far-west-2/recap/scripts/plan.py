"""Répartit les temps musicaux : photos 4 temps, vidéos selon leur longueur et leur poids, total = durée de la musique."""
import json, subprocess, sys, os
sys.path.insert(0, 'scripts'); from shots import *
B = 60 / BPM
def beat(k): return PHASE + k * B
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','../rushes/'+f]))
items = []
for f, lab, opt in ORDER:
    if f.endswith('.mp4'):
        cap = int((dur(f) - 0.5) / B)
        items.append(dict(f=f, lab=lab, opt=opt, cap=cap, b=min(cap, opt.get('w', 8))))
    else:
        items.append(dict(f=f, lab=lab, opt=opt, cap=6, b=4))
items[0]['b'] = INTRO_BEATS + 2  # premier plan porte le titre
target = END_START_BEAT
tot = sum(x['b'] for x in items)
i = 0
while tot != target:
    step = 1 if tot < target else -1
    if step > 0:
        cands = [x for x in items[1:] if x['b'] < x['cap']]
        cands.sort(key=lambda x: not x['f'].endswith('.mp4'))
    else:  # raccourcir d'abord les vidéos (jusqu'à 6 temps), puis les photos (jusqu'à 3)
        cands = [x for x in items[1:] if x['f'].endswith('.mp4') and x['b'] > 6] or [x for x in items[1:] if x['b'] > 3]
    x = cands[i % len(cands)]; x['b'] += step; tot += step; i += 1
k = 0
for x in items:
    x['start'] = round(beat(k) if k else 0.0, 3); k += x['b']; x['end'] = round(beat(k), 3); x['d'] = round(x['end'] - x['start'], 3)
json.dump(dict(items=items, end_start=round(beat(END_START_BEAT), 3), total=MUSIC_END), open('plan.json', 'w'), indent=1)
print(len(items), 'plans ; fin', beat(END_START_BEAT), '; photos', sorted(set(x['b'] for x in items if x['f'].endswith('jpg'))), '; vidéos', [(x['f'][3:6], x['b']) for x in items if x['f'].endswith('mp4')])
