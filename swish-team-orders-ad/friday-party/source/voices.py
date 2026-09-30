"""Speak every line with Kokoro (offline neural TTS), place it on the timeline, and export:
  dialogue.wav   48 kHz mono dialogue stem
  dialogue.json  line timings + a 60 fps mouth-open envelope per speaker (drives lip-sync in film.html)
usage: python3 voices.py /path/to/kokoro-v1.0.onnx /path/to/voices-v1.0.bin
"""
import json
import sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro
from script import CAST, LINES, CROWD

DUR, SR, FPS = 45.0, 48000, 60
k = Kokoro(sys.argv[1], sys.argv[2])
N = int(DUR * SR)
mix = np.zeros(N)
speak = {name: np.zeros(int(DUR * FPS)) for name in CAST}
out_lines = []


def tts(text, voice, speed):
    a, sr = k.create(text, voice=voice, speed=speed, lang='en-us' if voice[0] == 'a' else 'en-gb')
    a = resample_poly(a, SR, sr)
    # trim leading/trailing silence
    thr = 0.01 * np.max(np.abs(a))
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 2400]


def place(a, t0, who, gain=1.0):
    i0 = int(t0 * SR)
    n = min(len(a), N - i0)
    mix[i0:i0 + n] += a[:n] * gain
    # mouth envelope: RMS per video frame, compressed so small syllables still move the lips
    hop = SR // FPS
    for f in range(n // hop):
        seg = a[f * hop:(f + 1) * hop]
        v = np.sqrt(np.mean(seg ** 2))
        fi = int(t0 * FPS) + f
        if fi < len(speak[who]):
            speak[who][fi] = max(speak[who][fi], v)


for i, (lid, who, t0, text) in enumerate(LINES):
    nxt = LINES[i + 1][2] if i + 1 < len(LINES) else DUR - 0.3
    room = nxt - t0 - 0.12
    speed = 1.05
    a = tts(text, CAST[who][0], speed)
    while len(a) / SR > room and speed < 1.3:
        speed += 0.05
        a = tts(text, CAST[who][0], speed)
    place(a, t0, who)
    out_lines.append({'id': lid, 'who': who, 'text': text, 't0': round(t0, 3), 't1': round(t0 + len(a) / SR, 3), 'speed': round(speed, 2)})
    print(f'{lid} {who:7s} {t0:6.2f}-{t0 + len(a) / SR:6.2f}s (room {room:.2f}) x{speed:.2f}  {text}')

for cid, t0, parts in CROWD:
    for j, (who, text) in enumerate(parts):
        a = tts(text, CAST[who][0], 1.1)
        place(a, t0 + j * 0.07 + np.random.default_rng(j).uniform(0, 0.12), who, 0.55)
    out_lines.append({'id': cid, 'who': 'crowd', 'text': ' / '.join(p[1] for p in parts), 't0': t0, 't1': t0 + 1.0})

# normalise envelopes per speaker to 0..1 with a soft knee
env = {}
for who, e in speak.items():
    if e.max() > 0:
        e = e / np.percentile(e[e > 0], 95)
        e = np.clip(e, 0, 1) ** 0.6
        e = np.convolve(e, [0.25, 0.5, 0.25], mode='same')
    env[who] = [round(float(x), 2) for x in e]

mix /= max(1e-9, np.max(np.abs(mix))) / 0.9
sf.write('dialogue.wav', mix.astype(np.float32), SR)
json.dump({'lines': out_lines, 'mouth': env, 'fps': FPS}, open('dialogue.json', 'w'))
print('wrote dialogue.wav + dialogue.json')
