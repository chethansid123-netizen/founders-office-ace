"""Original background music for the reels, synthesised from scratch (no samples, no copyrighted material).

    python3 music.py <out_dir>

Writes diwali.wav, checkin.wav, jobs.wav, men.wav (44.1 kHz stereo, 16-bit).
"""
import sys
import wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def hz(semitones_from_a4):
    return 440.0 * 2 ** (semitones_from_a4 / 12)


NOTE = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}


def n(name, octave):
    return hz(NOTE[name] + 12 * (octave - 4))


def place(buf, sig, start):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


# ---------- instruments ----------
def piano(f, dur=3.0, vel=0.6):
    t = t_axis(dur)
    out = np.zeros_like(t)
    B = 0.0004
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 12000:
            break
        out += (1 / k ** 1.25) * np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.9 + 0.55 * k))
    out *= np.minimum(1, t / 0.004)
    out += 0.02 * rng.standard_normal(len(t)) * np.exp(-t / 0.01)  # hammer
    return vel * out / 2.2


def epiano(f, dur=2.5, vel=0.5):
    t = t_axis(dur)
    idx = 1.6 * np.exp(-t / 0.35)
    out = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t / 1.4)
    out += 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.5)
    out *= np.minimum(1, t / 0.006)
    return vel * out / 1.4


def santoor(f, dur=2.6, vel=0.5):
    """Two slightly detuned struck strings per note, like a santoor course."""
    t = t_axis(dur)
    out = np.zeros_like(t)
    for det in (-0.0009, 0.0011):
        for k, a in zip((1, 2, 3, 4, 5), (1, 0.5, 0.33, 0.18, 0.1)):
            out += a * np.sin(2 * np.pi * k * f * (1 + det) * t) * np.exp(-t * (1.1 + 0.9 * k))
    out *= np.minimum(1, t / 0.002)
    return vel * out / 3.2


def bell(f, dur=4.0, vel=0.25):
    t = t_axis(dur)
    out = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in ((1, 1, 0.9), (2.76, 0.45, 1.6), (5.4, 0.25, 2.6), (8.9, 0.1, 4)))
    return vel * out * np.minimum(1, t / 0.002) / 1.8


def tanpura(f, dur=5.0, vel=0.24):
    """Bright drone pluck with a slowly moving harmonic peak (a rough 'jawari' buzz)."""
    t = t_axis(dur)
    out = np.zeros_like(t)
    peak = 6 + 5 * np.sin(2 * np.pi * 0.35 * t)
    for k in range(1, 24):
        w = np.exp(-((k - peak) ** 2) / 18) + 0.6 / k
        out += w * np.sin(2 * np.pi * k * f * t + k)
    out *= np.exp(-t / 3.2) * np.minimum(1, t / 0.01)
    return vel * out / 6


def pad(freqs, dur, vel=0.12):
    t = t_axis(dur)
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0, 0.005):
            for k in range(1, 7):
                out += (1 / k ** 1.6) * np.sin(2 * np.pi * k * f * (1 + det) * t + rng.uniform(0, 6))
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    return vel * out * env / (len(freqs) * 6)


def kick(vel=0.6):
    t = t_axis(0.35)
    fr = 50 + 70 * np.exp(-t / 0.04)
    return vel * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.12)


def hat(vel=0.06):
    t = t_axis(0.08)
    x = rng.standard_normal(len(t))
    x = np.diff(np.concatenate([[0], x]))
    return vel * x * np.exp(-t / 0.018)


# ---------- mixing ----------
def reverb(x, sec=2.4, wet=0.28):
    L = int(sec * SR)
    t = np.arange(L) / SR
    out = []
    for ch in range(2):
        ir = rng.standard_normal(L) * np.exp(-t * 3.2 / sec)
        ir[: int(0.012 * SR)] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        size = 1 << int(np.ceil(np.log2(len(x) + L)))
        y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
        out.append((1 - wet) * x + wet * y)
    return np.stack(out, axis=1)


def master(st, fade_in=0.6, fade_out=1.8):
    n_ = len(st)
    t = np.arange(n_) / SR
    env = np.minimum(1, t / fade_in) * np.minimum(1, (n_ / SR - t) / fade_out)
    st = st * env[:, None]
    st = st / (np.max(np.abs(st)) + 1e-9) * 0.84
    return st


def write(path, st):
    data = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


# ---------- tracks ----------
def diwali(sec=17.6):
    """Raga Bhupali-flavoured (Sa Re Ga Pa Dha) santoor phrase over a tanpura drone, Sa = D."""
    buf = np.zeros(int(sec * SR))
    sa = n("D", 3)
    pa = sa * 1.5
    t = 0.0
    while t < sec:
        for f, d in ((pa / 2, 1.1), (sa, 1.1), (sa, 1.1), (sa / 2, 1.3)):
            place(buf, tanpura(f), t)
            t += d
    scale = {"S": 1, "R": 9 / 8, "G": 5 / 4, "P": 3 / 2, "D": 5 / 3, "S'": 2, "R'": 9 / 4}
    phrase = ["G", "R", "S", "R", "G", "P", "G", "", "D", "P", "G", "R", "S", "", "R", "G", "P", "D", "S'", "D", "P", "G", "R", "S"]
    beat = 0.5
    start = 1.2
    for i, sw in enumerate(phrase):
        if sw:
            place(buf, santoor(sa * 2 * scale[sw], vel=0.55 if i % 4 == 0 else 0.42), start + i * beat)
            if i % 4 == 0:
                place(buf, santoor(sa * 4 * scale[sw], vel=0.12), start + i * beat + 0.12)
    for bt in (0.4, 6.4, 12.4):
        place(buf, bell(sa * 4, vel=0.18), bt)
    return master(reverb(buf, 2.8, 0.32))


def checkin(sec=19.2, bpm=84):
    """Soft lo-fi: Fmaj7 Em7 Dm7 Cmaj7 on electric piano, gentle kick and hat, vinyl texture."""
    buf = np.zeros(int(sec * SR))
    b = 60 / bpm
    chords = [("F", "A", "C", "E"), ("E", "G", "B", "D"), ("D", "F", "A", "C"), ("C", "E", "G", "B")]
    bar = 4 * b
    t = 0.0
    i = 0
    while t < sec:
        ch = chords[i % 4]
        for k, name in enumerate(ch):
            oct_ = 3 if k == 0 else 4
            place(buf, epiano(n(name, oct_), dur=bar + 0.6, vel=0.32), t + k * 0.012)
        place(buf, epiano(n(ch[0], 2), dur=bar, vel=0.35), t)
        for q in range(4):
            if q in (0, 2):
                place(buf, kick(0.5), t + q * b)
            place(buf, hat(0.05), t + q * b + b / 2)
        # little melody on the last two beats
        place(buf, epiano(n(ch[2], 5), dur=1.0, vel=0.12), t + 3 * b)
        t += bar
        i += 1
    clicks = np.zeros_like(buf)
    idx = rng.integers(0, len(buf), size=int(sec * 9))
    clicks[idx] = rng.uniform(-0.25, 0.25, size=len(idx))
    hiss = 0.004 * rng.standard_normal(len(buf))
    buf = buf + 0.08 * clicks + hiss
    return master(reverb(buf, 1.8, 0.22))


def piano_track(chords, sec, bpm, top_line, pad_vel=0.1):
    buf = np.zeros(int(sec * SR))
    b = 60 / bpm
    bar = 4 * b
    t = 0.0
    i = 0
    while t < sec:
        root, third, fifth = chords[i % len(chords)]
        place(buf, piano(n(root, 2), dur=bar + 1, vel=0.5), t)
        arp = [n(root, 3), n(fifth, 3), n(third, 4), n(fifth, 4)]
        for q in range(8):
            place(buf, piano(arp[q % 4], dur=2.4, vel=0.3 if q % 2 else 0.38), t + q * b / 2)
        place(buf, pad([n(root, 3), n(third, 3), n(fifth, 3)], bar + 0.8, vel=pad_vel), t)
        mel = top_line[i % len(top_line)]
        if mel:
            place(buf, piano(n(mel, 5), dur=3, vel=0.28), t + b * 2)
        t += bar
        i += 1
    return master(reverb(buf, 2.6, 0.3))


def jobs(sec=17.6):
    return piano_track([("A", "C", "E"), ("F", "A", "C"), ("C", "E", "G"), ("G", "B", "D")], sec, 76, ["E", "C", "G", "B"])


def men(sec=17.4):
    return piano_track([("E", "G", "B"), ("C", "E", "G"), ("G", "B", "D"), ("D", "F#", "A")], sec, 70, ["B", "", "D", "F#"], pad_vel=0.14)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for name, fn in (("diwali", diwali), ("checkin", checkin), ("jobs", jobs), ("men", men)):
        write(f"{out}/{name}.wav", fn())
        print(name, "ok")
