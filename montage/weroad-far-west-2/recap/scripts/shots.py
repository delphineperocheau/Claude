# Tous les médias du dossier, ordre chronologique (numérotation Drive, recalée sur l'EXIF).
# (fichier, étiquette lieu ou None, options). Durées calculées en temps musicaux par build (129 BPM).
ORDER = [
    ("000001.jpg", "Los Angeles", {}),
    ("000002.jpg", "Joshua Tree", {}), ("000003.jpg", None, {}), ("000004.jpg", None, {}), ("000005.jpg", None, {}),
    ("000006.jpg", "Route 66", {}), ("000007.jpg", None, {}), ("000008.jpg", None, {}), ("000009.mp4", None, {}),
    ("000010.jpg", None, {}), ("000011.jpg", None, {}), ("000012.jpg", None, {}), ("000013.jpg", None, {}),
    ("000014.jpg", None, {}), ("000015.jpg", None, {}), ("000016.jpg", None, {}),
    ("000017.jpg", "Grand Canyon", {}), ("000018.jpg", None, {}), ("000019.jpg", None, {}), ("000020.mp4", None, {"w": 10}),
    ("000021.mp4", "Monument Valley", {}), ("000022.jpg", None, {}), ("000023.jpg", None, {}), ("000024.mp4", None, {}),
    ("000025.jpg", None, {}), ("000026.jpg", None, {}), ("000027.jpg", None, {}), ("000028.jpg", None, {}), ("000029.jpg", None, {}),
    ("000030.jpg", "Horseshoe Bend", {}), ("000031.mp4", None, {}),
    ("000032.jpg", "Antelope Canyon", {}), ("000033.jpg", None, {}), ("000034.jpg", None, {}), ("000035.mp4", None, {"w": 10}),
    ("000036.mp4", "Bryce Canyon", {}), ("000037.jpg", None, {}), ("000038.jpg", None, {}), ("000039.jpg", None, {}),
    ("000040.mp4", None, {}), ("000041.jpg", None, {}), ("000042.jpg", None, {}), ("000043.jpg", None, {}), ("000044.jpg", None, {}),
    ("000045.mp4", None, {}),
    ("000046.jpg", "Las Vegas", {"crop": (0, 190, 947, 1830)}), ("000047.mp4", None, {}), ("000048.jpg", None, {}), ("000049.jpg", None, {}),
    ("000050.jpg", None, {}), ("000051.mp4", None, {"w": 10}), ("000052.mp4", None, {}), ("000053.jpg", None, {}), ("000054.jpg", None, {}),
    ("000055.jpg", "Death Valley", {}),
    ("000056.jpg", "Las Vegas", {}), ("000057.mp4", None, {"w": 12}), ("000070.jpg", None, {}), ("000058.mp4", None, {"w": 10}), ("000059.jpg", None, {}),
    ("000060.mp4", None, {}), ("000061.mp4", "Calico", {"w": 10}), ("000062.jpg", None, {}),
    ("000063.jpg", "Warner Bros. Studio", {}), ("000064.jpg", None, {}), ("000065.mp4", None, {}), ("000066.jpg", None, {}),
    ("000067.jpg", None, {}), ("000068.mp4", None, {}),
    ("000069.jpg", "Los Angeles", {}),
]
END_BG = "000071.jpg"
BPM, PHASE = 129.0, 0.22
INTRO_BEATS = 8          # le titre sur le premier plan
MUSIC_END = 174.13
END_START_BEAT = 362     # écran de fin (~168,6 s)
