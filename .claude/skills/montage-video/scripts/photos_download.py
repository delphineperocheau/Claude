"""Télécharge un album Google Photos partagé (lien photos.app.goo.gl/... ou photos.google.com/share/...).
Récupère TOUT l'album (la page ne montre que ~300 médias : la suite est paginée via batchexecute),
en qualité d'origine : =dv pour les vidéos, =d pour les photos (HEIC détecté).
Usage : python3 photos_download.py <lien_album> <dossier_sortie>
Reprise possible : <dossier>/manifest.json garde url -> fichier + horodatage (ms, UTC) ; les fichiers déjà là sont sautés."""
import re, sys, os, json, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

url, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

def get(u, data=None, headers=UA):
    return urllib.request.urlopen(urllib.request.Request(u, data=data, headers=headers), timeout=300)

r = get(url)
final, page = r.geturl(), r.read().decode("utf-8", "ignore")
key = urllib.parse.parse_qs(urllib.parse.urlparse(final).query).get("key", [None])[0]
m = re.search(r"AF_initDataCallback\(\{key: 'ds:1'.*?data:(.*?), sideChannel", page, re.S)
d = json.loads(m.group(1))
aid, tok = d[3][0], d[2]
print("album :", d[3][1])
items = [(it[1][0], it[2]) for it in d[1]]
while tok:
    freq = json.dumps([[["snAcKc", json.dumps([aid, tok, None, key]), None, "generic"]]])
    resp = get("https://photos.google.com/_/PhotosUi/data/batchexecute",
               urllib.parse.urlencode({"f.req": freq}).encode(),
               {**UA, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}).read().decode()
    line = [l for l in resp.split("\n") if l.startswith('[["wrb.fr"')][0]
    d = json.loads(json.loads(line)[0][2])
    items += [(it[1][0], it[2]) for it in d[1]]
    tok = d[2]
print(f"{len(items)} média(s) dans l'album")

mpath = os.path.join(out, "manifest.json")
man = json.load(open(mpath)) if os.path.exists(mpath) else {}
used = {v["file"] for v in man.values()}
n = len(man)
todo = []
for u, ts in items:
    if u in man and os.path.exists(os.path.join(out, man[u]["file"])):
        man[u]["ts"] = ts
        continue
    n += 1
    while any(f.startswith(f"photos-{n:03d}.") for f in used): n += 1
    todo.append((n, u, ts))

EXT = {"video/mp4": ".mp4", "video/quicktime": ".mov", "image/jpeg": ".jpg", "image/png": ".png",
       "image/webp": ".webp", "image/heic": ".heic", "image/heif": ".heic"}
def dl(job):
    i, b, ts = job
    for suffix, kind in (("=dv", "video"), ("=d", "image")):
        try:
            r = get(b + suffix)
        except Exception:
            continue
        ct = r.headers.get("Content-Type", "").split(";")[0]
        if kind == "video" and not ct.startswith("video/"):
            continue
        data = r.read()
        ext = EXT.get(ct, ".bin")
        if ext == ".bin" and data[4:12] in (b"ftypheic", b"ftypmif1", b"ftypheix"):
            ext = ".heic"
        name = f"photos-{i:03d}{ext}"
        open(os.path.join(out, name), "wb").write(data)
        return b, name, ts
    print("échec", b)
    return b, None, ts

with ThreadPoolExecutor(8) as ex:
    for b, name, ts in ex.map(dl, todo):
        if name:
            man[b] = {"file": name, "ts": ts}
            print(name)
json.dump(man, open(mpath, "w"), indent=0)
print(f"{len(man)} fichier(s) dans {out}")
