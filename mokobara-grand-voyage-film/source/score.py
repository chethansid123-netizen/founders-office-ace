"""Original score + sound design for the Mokobara Grand Voyage 45 s film.
Neo-soul house in D major, 106.667 BPM: 20 bars x 2.25 s = 45.000 s, locked to film.template.html.
Everything is synthesised here (no samples), so there is nothing to license.
usage: python3 score.py [out.wav]
"""
import sys
import wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

OUT = sys.argv[1] if len(sys.argv) > 1 else 'score.wav'
SR = 48000
DUR = 45.0
N = int(SR * DUR)
BT = 0.5625          # beat
BAR = 2.25           # bar
S16 = BT / 4
rng = np.random.default_rng(2027)


def bar(k):
    return k * BAR


def ta(d):
    return np.arange(int(SR * d)) / SR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _sos(kind, f, order=2):
    if kind == 'band':
        lo, hi = f
        return butter(order, [lo / (SR / 2), min(hi, SR / 2 - 200) / (SR / 2)], 'band', output='sos')
    return butter(order, min(f, SR / 2 - 200) / (SR / 2), kind, output='sos')


def lp(x, f, o=2): return sosfilt(_sos('low', f, o), x)
def hp(x, f, o=2): return sosfilt(_sos('high', f, o), x)
def bp(x, lo, hi, o=2): return sosfilt(_sos('band', (lo, hi), o), x)


class Bus:
    def __init__(self):
        self.L = np.zeros(N); self.R = np.zeros(N)

    def add(self, sig, t0, g=1.0, pan=0.0, st=None):
        """mono sig (or stereo tuple via st) at time t0, equal-power pan"""
        i0 = int(round(t0 * SR))
        if i0 >= N:
            return
        if st is None:
            l = r = sig
        else:
            l, r = st
        if i0 < 0:
            l = l[-i0:]; r = r[-i0:]; i0 = 0
        n = min(len(l), N - i0)
        gl = g * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
        gr = g * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
        self.L[i0:i0 + n] += l[:n] * gl
        self.R[i0:i0 + n] += r[:n] * gr


drums, music, lead, sfx = Bus(), Bus(), Bus(), Bus()
rev_send, dly_send = Bus(), Bus()


def send(bus, sig, t0, g, pan=0.0, rev=0.0, dly=0.0, st=None):
    bus.add(sig, t0, g, pan, st)
    if rev:
        rev_send.add(sig, t0, g * rev, pan, st)
    if dly:
        dly_send.add(sig, t0, g * dly, pan, st)


# ------------------------------------------------------------------ instruments
def rhodes(m, d, vel=1.0):
    """FM electric piano: 1:1 carrier/modulator with decaying index, bell-ish tine, stereo tremolo."""
    f = hz(m)
    rel = 0.35
    t = ta(d + rel)
    idx = (1.6 * vel) * np.exp(-t / 0.25) + 0.25
    mod = idx * np.sin(2 * np.pi * f * t)
    body = np.sin(2 * np.pi * f * t + mod)
    tine = 0.18 * vel * np.sin(2 * np.pi * f * 7.02 * t) * np.exp(-t / 0.05)
    env = np.minimum(1, t / 0.004) * (0.35 + 0.65 * np.exp(-t / 1.1))
    env *= np.where(t < d, 1.0, np.exp(-(t - d) / 0.12))
    s = (body + tine) * env * 0.32
    trem = 0.12 * np.sin(2 * np.pi * 4.6 * t)
    s2 = np.sin(2 * np.pi * f * 1.0012 * t + mod) * env * 0.32 + tine * env * 0.32
    return (s * (1 + trem), s2 * (1 - trem))


def pad(notes, d, bright=1400, g=1.0):
    t = ta(d)
    L = np.zeros_like(t); R = np.zeros_like(t)
    for m in notes:
        f = hz(m)
        for k, det in enumerate((-11, -4, 3, 10)):
            ff = f * 2 ** (det / 1200)
            ph = rng.uniform(0, 6.28)
            w = np.zeros_like(t)
            for h in range(1, 14):
                if ff * h > 9000:
                    break
                w += np.sin(2 * np.pi * ff * h * t + ph * h) / h
            if k % 2 == 0:
                L += w
            else:
                R += w
    env = np.minimum(1, t / 0.7) * np.minimum(1, (d - t) / 0.5)
    L, R = 0.6 * L + 0.4 * R, 0.6 * R + 0.4 * L
    L = lp(L, bright) * env; R = lp(R, bright) * env
    k = 0.05 * g / max(1, len(notes))
    return (L * k, R * k)


def pluck(m, d=0.6, vel=1.0):
    """glassy mallet: FM 1:3.5 with fast-decaying index + sine body"""
    f = hz(m)
    t = ta(d)
    idx = 2.2 * np.exp(-t / 0.06)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.002) * np.exp(-t / 0.28)
    return s * env * 0.3 * vel


def bass(m, d, vel=1.0):
    f = hz(m)
    t = ta(d)
    s = np.sin(2 * np.pi * f * t) + 0.28 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 3 * f * t)
    env = np.minimum(1, t / 0.006) * (0.55 + 0.45 * np.exp(-t / 0.18)) * np.minimum(1, (d - t) / 0.03)
    return np.tanh(s * 1.3) * env * 0.5 * vel


def kick(g=1.0):
    t = ta(0.5)
    f = 48 + 120 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2)
    click = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.003) * 0.25
    return np.tanh((body + click) * 1.5) * g


def clap():
    t = ta(0.4)
    n = bp(rng.standard_normal(len(t)), 900, 4200)
    e = sum(np.where(t >= o, np.exp(-(t - o) / 0.009), 0) for o in (0, 0.009, 0.019))
    e = e + np.where(t >= 0.026, 0.5 * np.exp(-(t - 0.026) / 0.1), 0)
    snare_tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4
    return n * e * 0.8 + snare_tone


def rim():
    t = ta(0.08)
    return (bp(rng.standard_normal(len(t)), 1500, 5000) * 0.5 + np.sin(2 * np.pi * 820 * t)) * np.exp(-t / 0.012) * 0.45


def shaker(acc=1.0):
    t = ta(0.09)
    return hp(rng.standard_normal(len(t)), 6500, 3) * np.exp(-t / 0.022) * np.minimum(1, t / 0.006) * 0.35 * acc


def ohat():
    t = ta(0.35)
    return hp(rng.standard_normal(len(t)), 7500, 3) * np.exp(-t / 0.1) * 0.3


def crash():
    t = ta(2.2)
    n = hp(rng.standard_normal(len(t)), 3500)
    metal = sum(np.sin(2 * np.pi * f * t) for f in (3120, 4420, 5870, 7150)) * 0.05
    return (n + metal) * np.exp(-t / 0.7) * 0.35


# ------------------------------------------------------------------ sound design
def bell(m, d=1.6, g=1.0):
    t = ta(d); f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dd) for r, a, dd in ((1, 1, 1.0), (2.0, .45, .6), (3.0, .22, .35), (4.2, .12, .2)))
    return s * np.minimum(1, t / 0.002) * 0.3 * g


def flapclick(g=1.0):
    t = ta(0.03)
    return (bp(rng.standard_normal(len(t)), 1800, 6000) + 0.4 * np.sin(2 * np.pi * rng.uniform(1100, 1600) * t)) * np.exp(-t / 0.005) * 0.35 * g


def whoosh(d, f0, f1, g=1.0):
    t = ta(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    ch = 30
    for c in range(ch):
        a = c * len(n) // ch; b = (c + 1) * len(n) // ch
        fc = f0 * (f1 / f0) ** (c / (ch - 1))
        out[a:b] = bp(n[max(0, a - 600):b], fc * 0.6, fc * 1.6)[-(b - a):]
    return out * np.sin(np.pi * t / d) ** 1.4 * g


def zip_sfx(d, closing=False):
    """zipper: accelerating train of tiny tooth clicks through a sweeping band"""
    out = np.zeros(int(SR * (d + 0.1)))
    tt = 0.0; k = 0
    while tt < d:
        p = tt / d
        rate = 55 + 260 * np.sin(np.pi * min(1, p * 1.05)) ** 0.7
        c = flapclick(0.5 + 0.5 * rng.random())
        c = bp(c, 2000 + 3000 * (p if closing else 1 - p), 9000)
        i = int(tt * SR); out[i:i + len(c)] += c[:len(out) - i]
        tt += 1 / rate; k += 1
    t = ta(d + 0.1)
    hiss = bp(rng.standard_normal(len(t)), 2500, 8000) * 0.12 * np.sin(np.pi * np.clip(t / d, 0, 1))
    return out + hiss


def thud(g=1.0):
    t = ta(0.6)
    f = 55 + 60 * np.exp(-t / 0.04)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18) + lp(rng.standard_normal(len(t)), 600) * np.exp(-t / 0.04) * 0.6) * g


def plip(m=86):
    t = ta(0.25)
    f = hz(m) * (1 + 0.6 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05) * 0.4


def riser(d):
    t = ta(d)
    n = whoosh(d, 300, 9000, 1.0)
    tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (2.5 * t / d)) / SR) * 0.25
    return (n + tone) * (t / d) ** 2


def reverse_swell(d):
    t = ta(d)
    return hp(rng.standard_normal(len(t)), 3000) * (t / d) ** 3 * 0.5


# ------------------------------------------------------------------ harmony
CH = {
    'Dmaj9': [57, 61, 64, 66, 69], 'Bm9': [57, 61, 62, 66, 69], 'Gmaj9': [54, 57, 59, 62, 66],
    'A13s': [55, 59, 62, 66, 69], 'Em9': [55, 59, 62, 66, 67], 'F#m7': [57, 61, 64, 66, 69],
}
ROOT = {'Dmaj9': 38, 'Bm9': 35, 'Gmaj9': 43, 'A13s': 45, 'Em9': 40, 'F#m7': 42}
PROG = ['Gmaj9', 'F#m7', 'Em9', 'A13s',
        'Dmaj9', 'Bm9', 'Gmaj9', 'A13s', 'Dmaj9', 'Bm9', 'Gmaj9', 'A13s', 'Dmaj9', 'Bm9',
        'Gmaj9', 'Em9', 'A13s', 'Dmaj9', 'Gmaj9', 'Dmaj9']
FULL = set(range(4, 14)) | {17, 18}          # bars with the full groove

# pads everywhere, brighter in the drop sections
for b, name in enumerate(PROG):
    send(music, None, bar(b), 1.0, rev=0.5, st=pad(CH[name], BAR + 0.4, 3600 if b in FULL else 1900, 1.3))

# Rhodes: sustained in intro / breakdown, syncopated comp in the groove
COMP = [(0, 1.3, 1.0), (1.5, 0.35, 0.7), (2.75, 0.35, 0.65), (3.5, 0.45, 0.8)]
for b, name in enumerate(PROG):
    if b in FULL:
        for off, d, v in COMP:
            for m in CH[name]:
                send(music, None, bar(b) + off * BT, 0.8 * v, rev=0.25, st=rhodes(m, d * BT * 1.6, v))
    elif b != 19:
        for j, m in enumerate(CH[name]):   # gentle strum
            send(music, None, bar(b) + j * 0.03, 0.72 if b >= 2 else 0.55, rev=0.4, st=rhodes(m, BAR * 0.95, 0.75))
# final chord rings out
for j, m in enumerate(CH['Dmaj9'] + [74]):
    send(music, None, bar(19) + j * 0.035, 0.55, rev=0.55, st=rhodes(m, 2.0, 0.85))

# bass
for b, name in enumerate(PROG):
    r = ROOT[name]
    if b in FULL:
        pat = [(0, 0.9, 0), (1.5, 0.4, 0), (2.0, 0.4, 12), (2.75, 0.35, 0), (3.5, 0.45, 7)]
        for off, d, iv in pat:
            send(music, bass(r + iv, d * BT * 1.5), bar(b) + off * BT, 0.5)
    elif b in (2, 3, 16):
        for off in (0, 2):
            send(music, bass(r, 1.6 * BT), bar(b) + off * BT, 0.45)
    elif b in (14, 15):
        send(music, bass(r, BAR * 0.95), bar(b), 0.55)
send(music, bass(38, 2.1), bar(19), 0.7)

# drums
KICKS = []
for b in range(20):
    t0 = bar(b)
    if b in FULL or b == 16:
        for q in range(4):
            drums.add(kick(), t0 + q * BT, 0.75); KICKS.append(t0 + q * BT)
        if b != 16:
            for q in (1, 3):
                send(drums, clap(), t0 + q * BT, 0.42, rev=0.35)
            for q in range(4):
                drums.add(ohat(), t0 + q * BT + BT / 2, 0.22, 0.25)
    elif b in (2, 3):
        for q in (0, 2):
            drums.add(kick(0.8), t0 + q * BT, 0.8); KICKS.append(t0 + q * BT)
        for q in (1, 3):
            send(drums, rim(), t0 + q * BT, 0.5, 0.15, rev=0.3)
    if b in FULL or b in (1, 2, 3, 14, 15, 16):
        for s in range(16):
            swing = 0.03 if s % 2 else 0.0
            acc = 1.0 if s % 4 == 2 else (0.7 if s % 2 == 0 else 0.5)
            drums.add(shaker(acc), t0 + s * S16 + swing, 0.75 if b != 1 else 0.45, -0.35)
    if b == 15:
        for q in (1, 3):
            send(drums, rim(), t0 + q * BT, 0.45, 0.2, rev=0.35)
drums.add(kick(1.1), bar(19), 1.0); KICKS.append(bar(19))
for tt in (bar(4), bar(12), bar(17)):
    send(drums, crash(), tt, 0.7, rev=0.3)
for s in range(8):                                   # snare fill into the spec rush
    send(drums, clap(), bar(11) + 2 * BT + s * S16, 0.18 + 0.05 * s, rev=0.3)
for s in range(8):                                   # build before the price drop
    send(drums, clap(), bar(16) + 2 * BT + s * S16, 0.16 + 0.05 * s, rev=0.3)

# hook melody: glassy pluck through a dotted-8th ping-pong delay
D5, E5, Fs5, G5, A5, B5 = 74, 76, 78, 79, 81, 83
PH = {
    'a': [(0, Fs5, 1.0), (1.0, E5, .5), (1.5, Fs5, .5), (2.0, A5, 1.5), (3.5, B5, .5)],
    'b': [(0, A5, .75), (0.75, Fs5, .75), (1.5, E5, 1.0), (2.5, D5, 1.5)],
    'c': [(0, D5, .5), (0.5, E5, .5), (1.0, Fs5, 1.0), (2.0, B5, 1.0), (3.0, A5, 1.0)],
    'd': [(0, A5, 1.5), (1.5, G5, .5), (2.0, Fs5, 1.0), (3.0, E5, 1.0)],
    'end': [(0, Fs5, .5), (0.5, E5, .5), (1.0, D5, 3.0)],
}
HOOK = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 12: 'a', 13: 'b', 14: 'c', 15: 'd', 17: 'a', 18: 'c', 19: 'end'}
for b, ph in HOOK.items():
    vel = 0.75 if b in (6, 7) else 1.0
    for off, m, d in PH[ph]:
        send(lead, pluck(m, max(0.5, d * BT * 1.4), vel), bar(b) + off * BT, 1.25, pan=0.05, rev=0.35, dly=0.45)
        send(lead, pluck(m + 12, 0.4, vel * 0.5), bar(b) + off * BT, 0.25, pan=-0.2, rev=0.3)
# 16th arpeggio lifts the spec rush
for b in (12, 13):
    tones = [x + 12 for x in CH[PROG[b]][1:]]
    for s in range(16):
        send(lead, pluck(tones[s % 4], 0.3, 0.55), bar(b) + s * S16, 0.28, pan=(0.5 if s % 2 else -0.5), rev=0.2)

# ------------------------------------------------------------------ sound design on the picture's timeline
# cold open: airport chime, plane pass, split-flap board
for j, m in enumerate((79, 76, 72)):
    send(sfx, bell(m, 1.8, 0.9), 0.05 + j * 0.34, 0.45, pan=0.1, rev=0.55)
plane = lp(np.cumsum(rng.standard_normal(int(SR * 4.8))) * 0.002, 900)
plane *= np.sin(np.pi * np.clip(ta(4.8) / 4.8, 0, 1)) ** 2
send(sfx, plane / (np.abs(plane).max() + 1e-9), 0.0, 0.18, pan=-0.3, rev=0.2)
CHARS = [('GOA', 0.15, 0.3), ('3 DAYS', 0.55, 0.3), ('2', 1.05, 0.45)]
for txt, t0, spin in CHARS:
    for j, c in enumerate(txt):
        if c == ' ':
            continue
        settle = t0 + spin + j * 0.07
        tt = t0
        while tt < settle:
            sfx.add(flapclick(0.6), tt, 0.35, pan=-0.4 + j * 0.12)
            tt += 0.045
        sfx.add(flapclick(1.0), settle, 0.55, pan=-0.4 + j * 0.12)
send(sfx, thud(0.6), bar(1), 0.5, rev=0.3)                    # "Two bags?"
for tt in (2.9, 3.2):
    send(sfx, plip(84), tt, 0.35, rev=0.3)
send(sfx, reverse_swell(1.2), bar(2) - 1.2, 0.35)
# range: bags slide in
send(sfx, whoosh(0.5, 400, 3000, 1.0), bar(2) - 0.05, 0.25, -0.4)
send(sfx, whoosh(0.5, 400, 3000, 1.0), bar(2) + 2 * BT - 0.05, 0.25, 0.4)
send(sfx, riser(1.3), bar(4) - 1.3, 0.4, rev=0.2)
send(sfx, whoosh(0.42, 300, 5000, 1.0), bar(4) - 0.42, 0.45)   # yellow wipe
send(sfx, thud(1.0), bar(4) + 0.55, 0.55, rev=0.25)             # bag lands
# anatomy
send(sfx, zip_sfx(0.55), bar(6), 0.55, pan=-0.1, rev=0.15)
for o in (0.35, 0.9, 1.45):
    send(sfx, thud(0.35), bar(6) + o + 0.5, 0.35, rev=0.2)
send(sfx, whoosh(0.5, 300, 2000, 0.8), bar(7) + 0.3, 0.3, -0.5)
send(sfx, whoosh(0.6, 2500, 300, 0.8), bar(8) + 0.2, 0.3)
send(sfx, thud(0.4), bar(8) + 0.85, 0.3)
send(sfx, plip(88), bar(9) + 0.95, 0.4, 0.4, rev=0.4)
for k, tt in enumerate((bar(6), bar(7), bar(8), bar(9) + 0.1, bar(9) + 0.6)):
    send(sfx, plip(90 + 2 * k), tt + 0.45, 0.22, 0.3, rev=0.3)   # litre meter ticks
send(sfx, thud(1.2), bar(10) + 0.33, 0.7, rev=0.2)              # base lands
rain = bp(rng.standard_normal(int(SR * 2.3)), 1500, 7000) * np.minimum(1, ta(2.3) / 0.3) * np.minimum(1, (2.3 - ta(2.3)) / 0.3)
send(sfx, rain, bar(11), 0.12, 0.2, rev=0.3)
for k in range(10):
    send(sfx, plip(84 + (k * 5) % 12), bar(11) + 0.1 + k * 0.2 + rng.uniform(0, .08), 0.18, rng.uniform(-.6, .6), rev=0.4)
send(sfx, zip_sfx(0.5, True), bar(11) + 0.2, 0.5, rev=0.15)
send(sfx, flapclick(1.3), bar(11) + 0.75, 0.6)                   # lock
# spec rush: shutter tick on every card
for i in range(8):
    send(sfx, flapclick(1.2), bar(12) + i * BT, 0.35, 0.3)
send(sfx, whoosh(0.35, 3000, 500, 0.8), bar(12) + 5 * BT + 0.1, 0.3)   # squeeze into cabin box
# lifestyle: flash, destination board, swatches
send(sfx, reverse_swell(0.8), bar(14) - 0.8, 0.4)
for d_, t0 in (('GOA', 33.75), ('COORG', 34.3125), ('HAMPI', 34.875), ('JAIPUR', 35.4375)):
    for j in range(len(d_)):
        tt = t0
        while tt < t0 + 0.18 + j * 0.035:
            sfx.add(flapclick(0.5), tt, 0.25, -0.3 + j * 0.1)
            tt += 0.035
for i in range(3):
    send(sfx, plip(86 + 3 * i), bar(16) + i * BT, 0.3, rev=0.35)
send(sfx, riser(1.5), bar(17) - 1.5, 0.4, rev=0.2)
send(sfx, whoosh(0.42, 300, 5000, 1.0), bar(17) - 0.42, 0.45)
# the zip shuts — sonic payoff of the value proposition
send(sfx, zip_sfx(0.9, True), bar(18) + 2 * BT, 0.7, pan=0.0, rev=0.2)
send(sfx, thud(0.5), bar(18) + 2 * BT + 0.92, 0.35)
# end card: logo bells
for j, m in enumerate((74, 78, 81, 86)):
    send(sfx, bell(m, 2.2, 0.8), bar(19) + 0.05 + j * 0.07, 0.3, -0.3 + j * 0.2, rev=0.6)

# ------------------------------------------------------------------ mix
def sidechain(n, times, depth=0.55, rel=0.16):
    g = np.ones(n)
    t = np.arange(n) / SR
    for tk in times:
        i0 = int(tk * SR); i1 = min(n, i0 + int(SR * 0.6))
        seg = t[i0:i1] - tk
        g[i0:i1] = np.minimum(g[i0:i1], 1 - depth * np.exp(-seg / rel))
    return g

sc = sidechain(N, KICKS)

# stereo reverb: decorrelated noise IR, 2.4 s, damped, 25 ms pre-delay
irt = ta(2.4)
def ir():
    x = rng.standard_normal(len(irt)) * np.exp(-irt / 0.55)
    x = lp(x, 6000) * 0.6 + lp(x, 2500) * 0.4
    x = np.concatenate([np.zeros(int(0.025 * SR)), x])
    return x / np.sqrt(np.sum(x ** 2))
irL, irR = ir(), ir()
revL = fftconvolve(rev_send.L, irL)[:N] * 0.55
revR = fftconvolve(rev_send.R, irR)[:N] * 0.55

# ping-pong dotted-8th delay
dly = int(round(0.75 * BT * SR))
dL = np.zeros(N); dR = np.zeros(N)
srcL, srcR = lp(dly_send.L, 5000), lp(dly_send.R, 5000)
for k in range(1, 6):
    g = 0.42 ** k
    sh = dly * k
    if sh >= N:
        break
    if k % 2:
        dR[sh:] += srcL[:N - sh] * g
    else:
        dL[sh:] += srcR[:N - sh] * g

musicL = (music.L + lead.L * 0.9) * sc
musicR = (music.R + lead.R * 0.9) * sc
mixL = drums.L * 0.9 + musicL + sfx.L + revL * sc + dL * 0.7
mixR = drums.R * 0.9 + musicR + sfx.R + revR * sc + dR * 0.7

# low-end mono (below 120 Hz) and a touch of air
lowM = lp((mixL + mixR) / 2, 120, 4)
mixL = hp(mixL, 120, 4) + lowM * 0.7
mixR = hp(mixR, 120, 4) + lowM * 0.7
# presence + air, then widen the sides
for _ in (0,):
    pl, pr = bp(mixL, 2000, 6000), bp(mixR, 2000, 6000)
    mixL += pl * 0.35 + hp(mixL, 8000) * 0.25; mixR += pr * 0.35 + hp(mixR, 8000) * 0.25
M = (mixL + mixR) / 2; Sd = hp((mixL - mixR) / 2, 200) * 1.15
mixL, mixR = M + Sd, M - Sd

# glue compressor (RMS, 2.2:1, fast attack / 150 ms release)
lvl = np.sqrt(lp(((mixL ** 2 + mixR ** 2) / 2), 8, 1).clip(1e-12))
thr = np.percentile(lvl, 70)
gain = np.where(lvl > thr, (lvl / thr) ** (1 / 2.2 - 1), 1.0)
gain = lp(gain, 6, 1)
mixL *= gain; mixR *= gain

# fades
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.02) * np.clip((DUR - t) / 0.9, 0, 1) ** 0.8
mixL *= fade; mixR *= fade

mix = np.stack([mixL, mixR])
mix *= (10 ** (-14.0 / 20)) / np.sqrt(np.mean(mix ** 2))
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
mix *= (10 ** (-1.0 / 20)) / np.max(np.abs(mix))
print('rms dBFS %.1f  peak %.2f' % (20 * np.log10(np.sqrt(np.mean(mix ** 2))), np.max(np.abs(mix))))
pcm = (mix.T * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', OUT, pcm.shape[0] / SR, 's')
