import json, subprocess, os, sys
from PIL import Image, ImageOps
sys.path.insert(0, 'scripts'); from shots import END_BG
P = json.load(open('plan.json'))
os.makedirs('media', exist_ok=True)
out = {}
jobs = P['items'] + [dict(f=END_BG, opt={}, d=6)]
for x in jobs:
    f, opt = x['f'], x['opt']; stem = f[:-4]
    if f.endswith('.mp4'):
        o = f'media/{stem}.mp4'
        p = json.loads(subprocess.check_output(['ffprobe','-v','error','-print_format','json','-show_format','-show_streams','../rushes/'+f]))
        v = [s for s in p['streams'] if s['codec_type'] == 'video'][0]
        D = float(p['format']['duration']); need = x['d'] + 0.4
        st = max(0, D / 2 - need / 2)
        grade = 'eq=contrast=1.05:saturation=1.12'
        if v['width'] > v['height']:   # paysage : fond flouté + image entière
            fc = (f'[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.08[bg];'
                  f'[b]scale=1080:-2,{grade}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]')
            args = ['-filter_complex', fc, '-map', '[v]']
        else:
            args = ['-vf', f'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{grade},fps=30,format=yuv420p']
        if not os.path.exists(o):
            subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{st:.2f}','-i','../rushes/'+f,'-t',f'{need:.2f}','-an',*args,'-c:v','libx264','-crf','18','-preset','fast',o], check=True)
        out[f] = dict(file=o, kind='video')
    else:
        o = f'media/{stem}.jpg'
        im = ImageOps.exif_transpose(Image.open('../rushes/' + f)).convert('RGB')
        if 'crop' in opt: im = im.crop(opt['crop'])
        land = im.width > im.height * 1.05
        if not os.path.exists(o):
            h = 2000 if land else max(1920, int(1080 * im.height / im.width) + 200)
            im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(o, quality=90)
        out[f] = dict(file=o, kind='photo', land=land)
json.dump(out, open('media/index.json', 'w'), indent=1)
print(len(out))
