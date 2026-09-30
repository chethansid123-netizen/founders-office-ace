"""Music bed + sound design + dialogue -> soundtrack.wav for 'Friday Party' (45 s).
The music ducks under every spoken line (sidechained to the dialogue stem), so voices always sit on top.
usage: python3 mix.py
"""
import json
import wave
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR, DUR = 48000, 45.0
N = int(SR * DUR)
rng = np.random.default_rng(45)
BPM = 116; BT = 60 / BPM; S16 = BT / 4


def ta(d): return np.arange(int(SR * d)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def filt(x, kind, f, o=2):
    if kind == 'band':
        return sosfilt(butter(o, [f[0] / (SR / 2), f[1] / (SR / 2)], 'band', output='sos'), x)
    return sosfilt(butter(o, f / (SR / 2), kind, output='sos'), x)


class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, x, t0, g=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= N or i < 0: return
        n = min(len(x), N - i)
        s.L[i:i + n] += x[:n] * g * np.cos((pan + 1) * np.pi / 4) * 1.414
        s.R[i:i + n] += x[:n] * g * np.sin((pan + 1) * np.pi / 4) * 1.414


music, sfx, rev = Bus(), Bus(), Bus()

# ---------------- instruments
def pluck(m, d=0.5, v=1.0):
    t = ta(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t + 1.6 * np.exp(-t / 0.05) * np.sin(2 * np.pi * f * 2 * t)) + 0.3 * np.sin(4 * np.pi * f * t)
    return s * np.exp(-t / 0.22) * np.minimum(1, t / 0.002) * 0.3 * v
def keys(m, d, v=1.0):
    t = ta(d + 0.3); f = hz(m)
    s = np.sin(2 * np.pi * f * t + (1.3 * np.exp(-t / 0.3) + .2) * np.sin(2 * np.pi * f * t))
    e = np.minimum(1, t / 0.004) * (0.4 + 0.6 * np.exp(-t / 0.9)) * np.where(t < d, 1, np.exp(-(t - d) / 0.1))
    return s * e * 0.22 * v
def bass(m, d):
    t = ta(d); f = hz(m)
    return np.tanh(1.3 * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t))) * np.minimum(1, t / .005) * (0.6 + 0.4 * np.exp(-t / .15)) * np.minimum(1, (d - t) / .02) * 0.45
def kick():
    t = ta(0.4); f = 50 + 110 * np.exp(-t / 0.03)
    return np.tanh(1.4 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18))
def clap():
    t = ta(0.3); n = filt(rng.standard_normal(len(t)), 'band', (1000, 4500))
    return n * (sum(np.where(t >= o, np.exp(-(t - o) / .008), 0) for o in (0, .01, .02)) + np.where(t > .025, .4 * np.exp(-(t - .025) / .08), 0)) * .7
def shaker(a=1.0):
    t = ta(0.08); return filt(rng.standard_normal(len(t)), 'high', 6500, 3) * np.exp(-t / .02) * .3 * a
def snap():
    t = ta(0.12); return (filt(rng.standard_normal(len(t)), 'band', (1500, 6000)) * np.exp(-t / .01)) * .6

CH = {'D': [62, 66, 69, 73], 'Bm': [59, 62, 66, 69], 'G': [59, 62, 67, 71], 'A': [61, 64, 67, 69]}
ROOT = {'D': 38, 'Bm': 35, 'G': 43, 'A': 45}
PROG = ['D', 'Bm', 'G', 'A']
BAR = 4 * BT
nb = int(40.3 / BAR) + 1
for b in range(nb):
    t0 = b * BAR
    if t0 > 40.3: break
    name = PROG[b % 4]
    full = t0 >= 3.0 and not (22.9 < t0 < 25.2)         # light intro, a breath at checkout
    for q in range(4):
        tq = t0 + q * BT
        if tq > 40.2: break
        if full: music.add(kick(), tq, 0.55)
        if q in (1, 3): music.add(snap() if not full else clap(), tq, 0.35, 0.1); rev.add(clap(), tq, 0.1)
        for s in range(4):
            music.add(shaker(1 if s == 2 else .6), tq + s * S16 + (0.02 if s % 2 else 0), 0.45, -0.3)
    for off, d in ((0, 1.4), (1.5, .4), (2.5, .5), (3.5, .4)):
        for m in CH[name]:
            music.add(keys(m, d * BT), t0 + off * BT, 0.55, 0.15); rev.add(keys(m, d * BT), t0 + off * BT, 0.12)
    if full:
        for k, (off, iv) in enumerate(((0, 0), (1.5, 0), (2, 12), (3, 7), (3.5, 0))):
            music.add(bass(ROOT[name] + iv, .45 * BT * 1.6), t0 + off * BT, 0.7)
    # happy whistle-like hook on the pluck, every other bar
    if b % 2 == 0 and t0 > 3:
        mel = [(0, 78), (0.5, 81), (1, 83), (2, 81), (2.5, 78), (3, 76)] if (b // 2) % 2 == 0 else [(0, 76), (0.5, 78), (1, 81), (2, 78), (3, 74)]
        for off, m in mel:
            music.add(pluck(m), t0 + off * BT, 0.4, -0.2); rev.add(pluck(m), t0 + off * BT, 0.15)

# ---------------- sound design
def noise(d): return rng.standard_normal(int(SR * d))
def tick(g=1.0, f0=2000, f1=7000):
    t = ta(0.03); return filt(noise(0.03), 'band', (f0, f1)) * np.exp(-t / .004) * g
def buzz(d=0.35):
    t = ta(d); return np.sin(2 * np.pi * 160 * t) * (np.sin(2 * np.pi * 22 * t) > 0) * np.minimum(1, (d - t) / .02) * .3
def popsnd(f=900):
    t = ta(.12); fr = f * (0.6 + 0.4 * np.exp(-t / .02)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .035) * .5
def bell(m, d=1.2):
    t = ta(d); f = hz(m)
    return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dd) for r, a, dd in ((1, 1, .8), (2, .4, .4), (3.01, .2, .25))) * .3
def whoosh(d, f0, f1):
    t = ta(d); n = noise(d); o = np.zeros_like(n); ch = 20
    for c in range(ch):
        a = c * len(n) // ch; b = (c + 1) * len(n) // ch; fc = f0 * (f1 / f0) ** (c / (ch - 1))
        o[a:b] = filt(n[max(0, a - 500):b], 'band', (fc * .6, min(fc * 1.6, 20000)))[-(b - a):]
    return o * np.sin(np.pi * t / d) ** 1.5
def step():
    t = ta(.09); return filt(noise(.09), 'low', 900) * np.exp(-t / .02) * .5

OFFICE = [(0, 26.35), (33.2, 40.3)]
for a, b in OFFICE:   # room tone + distant keyboards
    d = b - a
    tone = filt(noise(d), 'low', 700) * .025
    sfx.add(tone, a, 1.0)
    t = a
    while t < b - .1:
        sfx.add(tick(.25, 2500, 8000), t, 0.25, rng.uniform(-.6, .6)); t += rng.uniform(.07, .35)
# link lands on everyone's phone
for i, (n, tt) in enumerate({'Priya': 13.95, 'Neha': 14.0, 'Rahul': 14.05, 'Kavya': 14.1, 'Karan': 14.15, 'Sneha': 14.2, 'Vikram': 14.25, 'Aditi': 14.3}.items()):
    sfx.add(buzz(), tt, 0.55, -0.7 + i * 0.2)
ADD = [14.35, 14.9, 16.2, 17.1, 17.7, 19.0, 19.6, 20.3, 20.9]
for k, tt in enumerate(ADD):
    sfx.add(popsnd(800 + 70 * k), tt, 0.5, rng.uniform(-.5, .5)); sfx.add(bell(84 + k, .5), tt + .02, 0.25)
# phone scenes: taps, sheet, whatsapp send
for tt in (11.95, 13.1, 23.2):
    sfx.add(tick(1.4, 1500, 6000), tt, 0.7); sfx.add(popsnd(1300), tt, 0.3)
sfx.add(whoosh(.35, 500, 4000), 12.3, 0.3)
sfx.add(whoosh(.3, 800, 5000), 13.35, 0.35); sfx.add(bell(88, .6), 13.45, 0.35)
sfx.add(bell(84, .8), 23.3, .4); sfx.add(bell(91, .9), 23.42, .4)          # order placed
# kitchen: clatter + boxes sliding into bags
k = filt(noise(1.55), 'band', (800, 6000)) * .05; sfx.add(k, 23.6, 1.0)
for i in range(9):
    sfx.add(whoosh(.3, 600, 2500), 23.75 + i * .1, 0.18, -0.5 + i * .12)
sfx.add(tick(1.2, 300, 1500), 24.6, .6)
# notification + get up
sfx.add(bell(86, .7), 25.1, .4); sfx.add(buzz(.3), 25.15, .4)
# lobby: lift ding, doors, footsteps, scooter idle, bag rustle
sfx.add(bell(84, 1.6) + np.pad(bell(79, 1.6), (int(.25 * SR), 0))[:int(1.6 * SR)], 26.95, .5)
sfx.add(whoosh(.6, 300, 1200), 27.0, .35)
for tt in np.arange(27.2, 28.45, .19): sfx.add(step(), tt, .6, -.3)
for tt in np.arange(31.9, 32.95, .19): sfx.add(step(), tt, .6, .3)
idle = filt(np.sin(2 * np.pi * 38 * ta(5.8)) * (1 + .5 * np.sin(2 * np.pi * 9 * ta(5.8))) + noise(5.8) * .3, 'low', 400) * .05
sfx.add(idle, 26.35, 1.0, .5)
rust = filt(noise(.5), 'band', (2000, 9000)) * np.exp(-ta(.5) / .15) * .25
for tt in (29.55, 29.75, 29.95): sfx.add(rust, tt, .6)
sfx.add(whoosh(.6, 1500, 300), 32.6, .3)
# lunch: boxes opening
for tt in (33.5, 34.0, 34.6, 35.2): sfx.add(rust, tt, .35, rng.uniform(-.5, .5))
# end card: swish + sparkle chime
sfx.add(whoosh(.35, 900, 8000), 40.2, .6)
for j, m in enumerate((77, 81, 84, 89)): sfx.add(bell(m, 1.4), 40.35 + j * .055, .45, -.4 + j * .27); rev.add(bell(m, 1.4), 40.35 + j * .055, .3)
# scene-change swooshes
for tt in (11.0, 14.15, 21.65, 23.6, 26.35, 33.2):
    sfx.add(whoosh(.3, 600, 5000), tt - .15, .22)

# ---------------- dialogue + mix
dlg, dsr = sf.read('dialogue.wav'); assert dsr == SR
dlg = np.pad(dlg, (0, max(0, N - len(dlg))))[:N]
# presence EQ on voices
dlg = dlg + filt(dlg, 'band', (2000, 5000)) * .35
env = np.sqrt(filt(dlg ** 2, 'low', 6, 1).clip(0))
duck = 1 - 0.62 * np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
duck = filt(duck, 'low', 4, 1)

ir_t = ta(1.8); ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / .4); ir = filt(ir, 'low', 5000); ir /= np.sqrt((ir ** 2).sum())
rl = fftconvolve(rev.L, ir)[:N] * .5; rr = fftconvolve(rev.R, np.roll(ir, 400))[:N] * .5
end_fade = np.clip((DUR - ta(DUR)) / 1.2, 0, 1)
mL = (music.L * .42 + rl * .6) * duck * end_fade + sfx.L * .8 + dlg * 1.3
mR = (music.R * .42 + rr * .6) * duck * end_fade + sfx.R * .8 + dlg * 1.3
mix = np.stack([mL, mR])
mix *= 10 ** (-14 / 20) / np.sqrt(np.mean(mix ** 2))
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))
pcm = (mix.T * 32767).astype(np.int16)
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('soundtrack.wav', pcm.shape[0] / SR, 's  rms %.1f dBFS' % (20 * np.log10(np.sqrt(np.mean(mix ** 2)))))
