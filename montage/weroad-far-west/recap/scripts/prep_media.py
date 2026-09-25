import json, subprocess, os, sys
sys.path.insert(0, 'scripts'); from shots import SHOTS, END_BG, END
from PIL import Image
R = json.load(open('../work/ordered.json'))
os.makedirs('media', exist_ok=True)
out = {}
for k, d, _ in SHOTS + [(END_BG, END, None)]:
    x = R[k]
    if x['kind'] == 'video':
        f = f'media/s{k:03d}.mp4'
        need = d + 0.6
        st = max(0, x['dur'] / 2 - need / 2)
        if not os.path.exists(f):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.2f}', '-i', '../rushes/' + x['n'], '-t', f'{need:.2f}', '-an',
                '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.05:saturation=1.12,fps=30,format=yuv420p',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', f], check=True)
        out[k] = dict(file=f, kind='video', dur=min(need, x['dur']))
    else:
        f = f'media/s{k:03d}.jpg'
        im = Image.open('../' + x['src'])
        land = im.width > im.height
        if not os.path.exists(f):
            h = 2000 if land else int(2200 * max(1, (im.height / im.width) / (1920 / 1080)))
            im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
            im.save(f, quality=88)
        out[k] = dict(file=f, kind='photo', land=land)
json.dump(out, open('media/index.json', 'w'), indent=1)
print(len(out), 'médias')
