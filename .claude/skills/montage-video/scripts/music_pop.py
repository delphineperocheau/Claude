"""Musique pop entraînante synthétisée (120 BPM, C G Am F). Usage : python3 scripts/music.py <durée> <sortie.wav>"""
import numpy as np, sys, wave
D = float(sys.argv[1]); SR = 44100; B = 0.5
n = int((D + 1) * SR); mix = np.zeros((n, 2))
rng = np.random.default_rng(3)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t, pan=0.0, g=1.0):
    i = int(t * SR); j = min(n, i + len(sig))
    if i >= n: return
    s = sig[:j - i] * g
    mix[i:j, 0] += s * (1 - pan) / 1; mix[i:j, 1] += s * (1 + pan) / 1
def env(L, a=0.005, dcy=0.3):
    t = np.arange(L) / SR; e = np.exp(-t / dcy); na = int(a * SR); e[:na] *= np.linspace(0, 1, na); return e
def pluck(m, L=0.45):
    t = np.arange(int(L * SR)) / SR; f = mtof(m)
    return (np.sin(2*np.pi*f*t) + 0.4*np.sin(4*np.pi*f*t) + 0.15*np.sin(6*np.pi*f*t)) * env(len(t), 0.004, 0.16)
def pad(ms, L):
    t = np.arange(int(L * SR)) / SR; s = sum(np.sin(2*np.pi*mtof(m)*t*1.003) + np.sin(2*np.pi*mtof(m)*t*0.997) for m in ms)
    e = np.minimum(1, t / 0.4) * np.minimum(1, (L - t) / 0.4); return s * e / len(ms)
def bass(m, L=0.24):
    t = np.arange(int(L * SR)) / SR; f = mtof(m); s = np.sign(np.sin(2*np.pi*f*t)) * 0.5 + np.sin(2*np.pi*f*t)
    k = np.ones(40) / 40; s = np.convolve(s, k, 'same'); return s * env(len(t), 0.004, 0.12)
def kick():
    t = np.arange(int(0.35 * SR)) / SR; f = 50 + 90 * np.exp(-t / 0.04); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t / 0.12)
def clap():
    L = int(0.2 * SR); s = rng.standard_normal(L); s = s - np.convolve(s, np.ones(8)/8, 'same'); return s * env(L, 0.002, 0.06)
def hat():
    L = int(0.06 * SR); s = rng.standard_normal(L); s = s - np.convolve(s, np.ones(3)/3, 'same'); return s * env(L, 0.001, 0.018)
CH = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [60, 64, 69, 72]), (41, [60, 65, 69, 72])]
INTRO, OUTRO = 4.0, D - 4.5
bar = 0; t = 0.0
while t < D:
    root, notes = CH[bar % 4]
    add(pad([m - 12 for m in notes[:3]], 2.05), t, 0, 0.16)
    for s in range(8):
        tt = t + s * B / 2
        if tt >= D: break
        arp = notes[[0, 1, 2, 3, 2, 1, 2, 3][s]] + 12
        add(pluck(arp), tt, (-0.3 if s % 2 else 0.3), 0.20 if tt >= INTRO else 0.14)
        if INTRO <= tt < OUTRO:
            add(bass(root - 12 if s % 2 == 0 else root), tt, 0, 0.30)
            if s % 2 == 1: add(hat(), tt, 0.2, 0.10)
            if s % 2 == 0: add(kick(), tt, 0, 0.55)
            if s in (2, 6): add(clap(), tt, -0.1, 0.22)
    bar += 1; t += 4 * B
# accord final tenu
add(pad([48, 55, 60, 64, 67], 4.0), OUTRO + 0.0, 0, 0.12)
fade = np.ones(n); fe = int(D * SR); fs = int((D - 1.5) * SR)
fade[fs:fe] = np.linspace(1, 0, fe - fs); fade[fe:] = 0
mix *= fade[:, None]
mix = np.tanh(mix * 1.4); mix /= np.abs(mix).max() * 1.12
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix[:int(D*SR)] * 32767).astype('<i2').tobytes()); w.close()
