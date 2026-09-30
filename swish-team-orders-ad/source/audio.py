"""Soundtrack for the Swish Team Orders 15s ad.
128 BPM, 8 bars = 15.000s. Every hit is placed on the same timeline the animation uses (ad.template.html).
Sections: tension (bars 0-1) -> sparkle drop (bar 2) -> bright groove (bars 2-5) -> slams (bar 6) -> sonic logo + end chord (bar 7).
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
import wave

SR = 48000
DUR = 15.0
N = int(SR * DUR)
BPM = 128
B = 60 / BPM          # beat 0.46875
E8 = B / 2
E16 = B / 4
BAR = 4 * B
rng = np.random.default_rng(7)

L = np.zeros(N); R = np.zeros(N)        # dry bus
RV = np.zeros(N)                        # reverb send (mono)


def t_arr(d):
    return np.arange(int(SR * d)) / SR


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100) / (SR / 2), 'low', output='sos'), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), 'high', output='sos'), x)


def bp(x, f1, f2, order=2):
    return sosfilt(butter(order, [f1 / (SR / 2), min(f2, SR / 2 - 100) / (SR / 2)], 'band', output='sos'), x)


def add(sig, t0, gain=1.0, pan=0.0, rev=0.0):
    i0 = int(round(t0 * SR))
    if i0 >= N:
        return
    if i0 < 0:
        sig = sig[-i0:]; i0 = 0
    n = min(len(sig), N - i0)
    gl = gain * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
    gr = gain * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    L[i0:i0 + n] += sig[:n] * gl
    R[i0:i0 + n] += sig[:n] * gr
    if rev:
        RV[i0:i0 + n] += sig[:n] * gain * rev


def saw(f, d, detune_cents=0.0):
    t = t_arr(d)
    ff = f * 2 ** (detune_cents / 1200)
    nh = max(1, int((SR / 2 * 0.8) // ff))
    nh = min(nh, 40)
    out = np.zeros_like(t)
    ph = rng.uniform(0, 2 * np.pi)
    for k in range(1, nh + 1):
        out += np.sin(2 * np.pi * ff * k * t + ph * k) / k
    return out * 0.6


def env_ad(d, a=0.005, dec=0.2, sustain=0.0):
    t = t_arr(d)
    e = np.where(t < a, t / a, sustain + (1 - sustain) * np.exp(-(t - a) / dec))
    return e


# ---------------------------------------------------------------- drums
def kick(g=1.0):
    d = 0.45; t = t_arr(d)
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.22)
    click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * g


def clap():
    d = 0.35; t = t_arr(d)
    n = bp(rng.standard_normal(len(t)), 900, 3200)
    e = np.zeros_like(t)
    for off in (0, 0.011, 0.022):
        e += np.where(t >= off, np.exp(-(t - off) / 0.012), 0)
    e += np.where(t >= 0.03, 0.55 * np.exp(-(t - 0.03) / 0.12), 0)
    return n * e * 0.9


def hat(open_=False):
    d = 0.3 if open_ else 0.06; t = t_arr(d)
    n = hp(rng.standard_normal(len(t)), 7000, 3)
    return n * np.exp(-t / (0.09 if open_ else 0.018)) * 0.5


def crash():
    d = 1.8; t = t_arr(d)
    n = hp(rng.standard_normal(len(t)), 4000, 2)
    return n * np.exp(-t / 0.55) * 0.45


def boom():  # impact for pain cards / stamp
    d = 0.9; t = t_arr(d)
    f = 38 + 90 * np.exp(-t / 0.06)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    thump = lp(rng.standard_normal(len(t)), 900) * np.exp(-t / 0.05) * 0.8
    snap = bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.02) * 0.5
    return np.tanh((body + thump + snap) * 1.4)


# ---------------------------------------------------------------- sfx
def pop(f=900, g=1.0):
    d = 0.12; t = t_arr(d)
    fr = f * (0.55 + 0.45 * np.exp(-t / 0.02))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.035)
    return s * g


def blip(midi, g=1.0):  # item-added "collect" sound: bright pluck with octave
    d = 0.35; t = t_arr(d)
    f = hz(midi)
    s = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) + 0.18 * np.sin(2 * np.pi * 3 * f * t))
    s *= np.exp(-t / 0.09) * np.minimum(1, t / 0.002)
    return s * 0.5 * g


def bell(midi, d=1.4, g=1.0):
    t = t_arr(d); f = hz(midi)
    s = np.zeros_like(t)
    for ratio, amp, dec in ((1, 1, 0.9), (2.0, 0.5, 0.5), (3.01, 0.28, 0.3), (4.17, 0.18, 0.18), (5.43, 0.1, 0.1)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / dec)
    return s * np.minimum(1, t / 0.002) * 0.35 * g


def whoosh(d=0.35, f0=600, f1=6000, g=1.0, rise=True):
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    # time-varying band via chunked filtering
    out = np.zeros_like(n)
    chunks = 24
    for c in range(chunks):
        a = c * len(n) // chunks; b = (c + 1) * len(n) // chunks
        k = c / (chunks - 1)
        fc = f0 * (f1 / f0) ** (k if rise else 1 - k)
        out[a:b] = bp(n[max(0, a - 400):b], fc * 0.6, fc * 1.6)[-(b - a):]
    shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** (0.7 if rise else 1.2)
    if rise:
        shape = shape * (0.3 + 0.7 * t / d)
    return out * shape * g


def click(g=1.0):
    d = 0.03; t = t_arr(d)
    return hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.004) * g


def riser(d):
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n); chunks = 40
    for c in range(chunks):
        a = c * len(n) // chunks; b = (c + 1) * len(n) // chunks
        fc = 300 * (9000 / 300) ** (c / (chunks - 1))
        out[a:b] = bp(n[max(0, a - 400):b], fc * 0.7, fc * 1.4)[-(b - a):]
    tone_f = 110 * 2 ** (3 * t / d)
    tone = np.sin(2 * np.pi * np.cumsum(tone_f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(tone_f * 1.5) / SR)
    e = (t / d) ** 2.2
    return (out * 0.8 + tone * 0.25) * e


# ---------------------------------------------------------------- music
F_MAJ = {  # chord tones (midi) for stabs, bass root
    'F': ([65, 69, 72, 77], 41), 'C': ([64, 67, 72, 76], 36), 'Dm': ([62, 65, 69, 74], 38), 'Bb': ([62, 65, 70, 74], 34),
    'Gm': ([62, 67, 70, 74], 43),
}


def stab(notes, d=0.32, cutoff=3200, g=1.0):
    s = sum(saw(hz(m), d, -9) + saw(hz(m), d, 9) for m in notes) / len(notes)
    s = lp(s, cutoff)
    return s * env_ad(d, 0.004, 0.11) * g


def bass_note(midi, d=E8 * 0.95, g=1.0):
    t = t_arr(d); f = hz(midi)
    s = 0.7 * np.sin(2 * np.pi * f * t) + 0.5 * lp(saw(f, d), 700)
    return s * env_ad(d, 0.004, 0.12, 0.3) * np.minimum(1, (d - t) / 0.01) * g


def pad(notes, d, g=1.0):
    t = t_arr(d)
    s = sum(saw(hz(m), d, -12) + saw(hz(m), d, 12) for m in notes) / len(notes)
    s = lp(s, 1800)
    e = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.3)
    return s * e * g


# ---- bars 0-1: tension (D minor pulse) ----
for i in range(int(3.6 / E8)):
    tt = i * E8
    note = 38 if (i // 4) % 2 == 0 else 37  # D - C# rocking, uneasy
    add(lp(bass_note(note, E8 * 0.9, 0.9), 400 + 900 * tt / 3.6), tt, 0.55)
for i in range(int(3.55 / E16)):
    add(hat(False), i * E16, 0.16 + 0.08 * (i % 2 == 0), pan=0.25)
# tick-tock clock feel
for i in range(int(3.6 / B)):
    add(click(0.5), i * B, 0.5, pan=-0.3)

# chat pops (match BUB_T in the animation; negative ones are pre-roll)
BUB_T = [-.5, -.25, .15, .40, .60, .78, .94, 1.08, 1.20, 1.32, 1.44, 1.56]
for i, bt in enumerate(BUB_T):
    if bt >= 0:
        add(pop(700 + (i * 137) % 600), bt, 0.55, pan=((i * 0.37) % 1.2) - 0.6)
add(pop(820), 0.0, 0.5, pan=-0.3)   # first frame notification
add(bell(88, 0.4, 0.5), 0.02, 0.35, pan=0.2, rev=0.2)

# hook word emphasis: soft hit on "lunch orders."
add(boom() * 0.5, 0.84, 0.45)

# pain card slams
for tt in (1.875, 2.34375, 2.8125):
    add(boom(), tt, 0.95)
    add(stab(F_MAJ['Dm'][0], 0.4, 1400, 1.0), tt, 0.35, rev=0.25)
    add(clap(), tt, 0.35, rev=0.3)

# riser into the drop, with a breath of silence before it
add(riser(0.78), 2.95, 0.55, rev=0.2)
add(whoosh(0.4, 500, 7000, 0.9, True), 3.36, 0.5)

# ---- 3.75: the sparkle drop (sonic logo, part 1) ----
DROP = 3.75
add(whoosh(0.32, 900, 8000, 1.0, False), DROP - 0.05, 0.6, pan=-0.2)
add(crash(), DROP, 0.6, rev=0.3)
add(kick(1.2), DROP, 1.0)
for j, m in enumerate((77, 81, 84, 89)):   # F A C F sparkle arpeggio
    add(bell(m, 1.2), DROP + 0.03 + j * 0.055, 0.5, pan=-0.4 + j * 0.27, rev=0.5)

# ---- bars 2-5: groove ----
PROG = ['F', 'C', 'Dm', 'Bb']
GROOVE_END = 11.25
for bar in range(4):
    t0 = DROP + bar * BAR
    chord, root = F_MAJ[PROG[bar]]
    for b in range(4):
        tb = t0 + b * B
        add(kick(), tb, 0.95)
        if b in (1, 3):
            add(clap(), tb, 0.5, rev=0.25)
        add(hat(True), tb + E8, 0.28, pan=0.3)
        for s16 in range(4):
            add(hat(False), tb + s16 * E16, 0.12 + 0.06 * (s16 == 2), pan=-0.25)
    # bass: 8ths, octave bounce
    for k in range(8):
        m = root + (12 if k % 2 else 0)
        add(bass_note(m, E8 * 0.9, 1.0), t0 + k * E8, 0.55)
    # stab rhythm: syncopated (1, 1.75(&a), 2.5, 3.5, 4.25)
    for off in (0, 0.75, 1.5, 2.5, 3.25):
        add(stab(chord, 0.28, 3600), t0 + off * B, 0.33, pan=0.1, rev=0.2)

# ---- step SFX (match the animation) ----
add(whoosh(0.4, 300, 2500, 0.8, True), 5.35, 0.35)            # phone rises
add(click(1.0), 6.00, 0.8); add(pop(1200), 6.00, 0.35)         # tap
add(whoosh(0.3, 400, 3000, 0.7, True), 6.12, 0.3)             # sheet
add(click(0.8), 6.62, 0.6)                                     # copy
add(whoosh(0.36, 800, 6000, 0.8, True), 6.66, 0.4, pan=-0.3)  # link flies
add(bell(91, 0.5, 0.6), 6.98, 0.35, pan=-0.4, rev=0.3)        # message sent
add(whoosh(0.25, 600, 4000, 0.7, False), 7.26, 0.3)           # swipe to cart
ITEM_T = [7.5 + i * E8 for i in range(8)]
PENTA = [77, 79, 81, 84, 86, 89, 91, 93]  # rising F major pentatonic: every add feels like progress
for i, it in enumerate(ITEM_T):
    add(blip(PENTA[i]), it, 0.55, pan=(-0.35 if i % 2 == 0 else 0.35), rev=0.2)
    add(pop(900 + 60 * i), it, 0.25)
add(whoosh(0.25, 600, 4000, 0.7, False), 9.32, 0.3)           # swipe to tracking
for i in range(5):
    add(click(0.6), 9.62 + i * 0.09, 0.35)                     # bill rows
add(boom(), 10.50, 0.9)                                        # stamp
add(clap(), 10.50, 0.3)
add(whoosh(0.3, 500, 8000, 1.0, True), 10.96, 0.6)            # sparkle wipe 2

# ---- bar 6: slams ----
SLAMS = [11.25, 11.71875, 12.1875]
SL_CH = ['Bb', 'C', 'Dm']
for tt, ch in zip(SLAMS, SL_CH):
    add(kick(1.2), tt, 1.0)
    add(stab(F_MAJ[ch][0], 0.42, 4200, 1.2), tt, 0.5, rev=0.35)
    add(bass_note(F_MAJ[ch][1], 0.4, 1.0), tt, 0.6)
    add(clap(), tt, 0.45, rev=0.3)
    for s16 in range(4):
        add(hat(False), tt + s16 * E16, 0.12, pan=-0.2)
add(riser(0.36) * 0.8, 12.30, 0.35)
add(kick(1.3), 12.65625, 1.0)
add(boom(), 12.65625, 0.6)
add(crash(), 12.65625, 0.7, rev=0.3)
add(stab(F_MAJ['C'][0], 0.46, 5000, 1.3), 12.65625, 0.55, rev=0.35)
add(bass_note(36, 0.45, 1.0), 12.65625, 0.6)

# ---- bar 7: sonic logo + resolve ----
LOGO = 13.125
add(whoosh(0.34, 900, 8000, 1.0, False), LOGO - 0.06, 0.85, pan=0.2)
for j, m in enumerate((77, 81, 84, 89)):
    add(bell(m, 1.6), LOGO + 0.05 + j * 0.055, 0.55, pan=-0.4 + j * 0.27, rev=0.55)
add(kick(1.2), LOGO, 1.0)
add(crash(), LOGO, 0.55, rev=0.3)
add(pad(F_MAJ['F'][0], 15.0 - LOGO, 1.0), LOGO, 0.42, rev=0.3)
add(bass_note(41, 1.8, 1.0) * np.exp(-t_arr(1.8) / 0.9), LOGO, 0.6)
for b in range(1, 4):
    tb = LOGO + b * B
    add(kick(0.8), tb, 0.6)
    add(hat(True), tb + E8, 0.2, pan=0.3)
add(click(1.0), 14.42, 0.7)
add(bell(96, 1.0), 14.44, 0.45, pan=0.3, rev=0.5)               # CTA tap "ding"

# ---------------------------------------------------------------- mix
ir_t = t_arr(1.3)
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.35)
ir = lp(ir, 5000)
ir /= np.sqrt(np.sum(ir ** 2))
wet = fftconvolve(RV, ir)[:N] * 0.35
wetL = wet
wetR = np.concatenate([np.zeros(int(0.011 * SR)), wet])[:N]
mixL = L + wetL
mixR = R + wetR

# gentle fade at the very end to avoid a click
fade = np.ones(N)
fn = int(0.12 * SR)
fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
mixL *= fade; mixR *= fade

# loudness: aim roughly for streaming level, then soft-limit
mix = np.stack([mixL, mixR])
rms = np.sqrt(np.mean(mix ** 2))
target = 10 ** (-15.0 / 20)
mix *= target / rms
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
peak = np.max(np.abs(mix))
mix *= (10 ** (-1.0 / 20)) / peak
print('rms dBFS', 20 * np.log10(np.sqrt(np.mean(mix ** 2))), 'peak', np.max(np.abs(mix)))

pcm = (mix.T * 32767).astype(np.int16)
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote soundtrack.wav', pcm.shape[0] / SR, 's')
