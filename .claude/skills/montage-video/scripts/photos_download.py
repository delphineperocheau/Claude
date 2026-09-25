"""Télécharge un album Google Photos partagé (lien photos.app.goo.gl/... ou photos.google.com/share/...).
Récupère chaque média en qualité d'origine : =dv pour les vidéos, =d pour les photos.
Usage : python3 photos_download.py <lien_album> <dossier_sortie>
Limite : fonctionne sur la page publique de l'album ; un album non partagé par lien renvoie 0 média."""
import re, sys, os, urllib.request

url, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120)

page = get(url).read().decode("utf-8", "ignore")
# médias de l'album : /pw/ (les avatars sont sous /a/)
bases = []
for m in re.findall(r"https://lh3\.googleusercontent\.com/pw/[A-Za-z0-9_\-]+", page):
    if m not in bases:
        bases.append(m)
print(f"{len(bases)} média(s) trouvé(s)")
for i, b in enumerate(bases, 1):
    done = False
    for suffix, kind in (("=dv", "video"), ("=d", "image")):
        try:
            r = get(b + suffix)
        except Exception:
            continue
        ct = r.headers.get("Content-Type", "")
        if kind == "video" and not ct.startswith("video/"):
            continue
        ext = {"video/mp4": ".mp4", "video/quicktime": ".mov", "image/jpeg": ".jpg", "image/png": ".png",
               "image/webp": ".webp", "image/heic": ".heic", "image/heif": ".heic"}.get(ct.split(";")[0], ".bin")
        data = r.read()
        if ext == ".bin" and data[4:12] in (b"ftypheic", b"ftypmif1", b"ftypheix"):
            ext = ".heic"
        path = os.path.join(out, f"photos-{i:03d}{ext}")
        with open(path, "wb") as f:
            f.write(data)
        print(path, ct, os.path.getsize(path))
        done = True
        break
    if not done:
        print("échec", b)
