# Plans dans l'ordre chronologique : (fichier dans ../rushes, durée, étiquette lieu ou None, options)
# options vidéo : ss = début (s), crop = recadrage ffmpeg avant mise au format 1080x1920
SHOTS = [
    ("photos-701.heic", 4.0, None, {}),                      # aile d'avion au coucher du soleil (titre)
    ("photos-693.heic", 1.5, "Santa Monica", {}),
    ("photos-662.jpg", 2.0, "Beverly Hills", {}),              # selfie de groupe
    ("photos-655.heic", 1.5, "Hollywood", {}),
    ("photos-636.heic", 1.5, "Joshua Tree", {}),
    ("photos-618.heic", 2.0, None, {}),                      # groupe à Skull Rock
    ("photos-592.heic", 2.0, None, {}),                      # marche au coucher du soleil
    ("photos-567.heic", 1.5, "Route 66", {}),                # âne sur la route
    ("photos-563.heic", 2.0, None, {}),                      # bisou à l'âne
    ("photos-539.heic", 1.5, None, {}),
    ("photos-506.heic", 1.5, "Grand Canyon", {}),            # selfie au lever du soleil
    ("photos-503.heic", 2.5, None, {}),                      # bras ouverts
    ("photos-485.heic", 1.5, None, {}),
    ("photos-430.heic", 2.0, "Monument Valley", {}),
    ("photos-415.heic", 1.5, None, {}),
    ("photos-383.heic", 2.0, "Horseshoe Bend", {}),
    ("photos-359.heic", 1.5, "Antelope Canyon", {}),
    ("photos-347.mp4", 1.5, None, {}),
    ("photos-316.mp4", 2.0, "Bryce Canyon", {}),
    ("photos-297.mp4", 1.5, None, {}),
    ("photos-261.mp4", 2.0, "Las Vegas", {}),
    ("photos-233.mp4", 1.5, None, {}),
    ("photos-232.mp4", 1.5, None, {}),
    ("photos-219.mp4", 2.0, "Death Valley", {}),
    ("photos-213.mp4", 1.5, None, {}),
    ("photos-202.mp4", 2.0, "Las Vegas", {}),                # toque « exigeant, mais facile aussi »
    ("photos-192.mp4", 1.5, None, {}),
    ("photos-180.mp4", 1.5, "Calico", {}),
    ("photos-169.jpg", 1.5, "Los Angeles", {}),
    ("photos-159.heic", 1.5, None, {}),
    ("photos-137.heic", 2.0, "Warner Bros. Studio", {}),
    ("photos-112.mp4", 1.5, None, {}),
    ("photos-095.mp4", 1.5, "Dodger Stadium", {}),
    ("photos-062.mp4", 1.5, "Universal Studios", {}),
    ("photos-042.heic", 1.5, None, {}),
    ("photos-032.mp4", 3.5, "Long Beach", {"ss": 5.4, "crop": "480:853:685:113"}),  # la baleine
    ("photos-035.heic", 2.0, None, {}),
    ("photos-014.heic", 2.0, "Los Angeles", {}),
    ("photos-007.heic", 2.5, None, {}),
]
END_BG = "photos-005.heic"
END = 4.5
