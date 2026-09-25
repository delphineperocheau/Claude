import json, subprocess, os, sys
sys.path.insert(0, 'scripts'); from shots import SHOTS, END_BG, END
from PIL import Image
os.makedirs('media', exist_ok=True)
out = {}
for n, d, _, opt in SHOTS + [(END_BG, END, None, {})]:
    stem, ext = os.path.splitext(n)
    if ext in ('.mp4', '.mov'):
        f = f'media/{stem}.mp4'
        dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', '../rushes/' + n]))
        need = d + 0.6
        st = opt.get('ss', max(0, dur / 2 - need / 2))
        vf = (f"crop={opt['crop']}," if 'crop' in opt else '') + 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.05:saturation=1.12,fps=30,format=yuv420p'
        if not os.path.exists(f):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.2f}', '-i', '../rushes/' + n, '-t', f'{need:.2f}', '-an', '-vf', vf,
                            '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', f], check=True)
        out[n] = dict(file=f, kind='video')
    else:
        f = f'media/{stem}.jpg'
        im = Image.open(f'../work/jpg/{stem}.jpg')
        land = im.width > im.height
        if not os.path.exists(f):
            h = 2000 if land else int(2200 * max(1, (im.height / im.width) / (1920 / 1080)))
            im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(f, quality=88)
        out[n] = dict(file=f, kind='photo', land=land)
json.dump(out, open('media/index.json', 'w'), indent=1)
print(len(out), 'médias')
