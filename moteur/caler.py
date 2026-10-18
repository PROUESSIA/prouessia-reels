"""Découpe un .wav Gemini (une prise) en segments de parole et les transcrit.
Usage : python3 caler.py fichier.wav [nb_phrases_attendues]"""
import os, sys, re, subprocess, json
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

ASR = os.environ.get('ASR_DIR', os.path.expanduser('~/asr/sherpa-onnx-whisper-small/'))


def segments(wav, seuil='-40dB', mini=0.3):
    out = subprocess.run(['ffmpeg', '-i', wav, '-af', f'silencedetect=noise={seuil}:d={mini}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    s, sr = sf.read(wav); D = len(s) / sr
    bornes, debut = [], 0.0
    if st and st[0] < 0.05:
        debut = en[0]; st, en = st[1:], en[1:]
    for i, a in enumerate(st):
        if a - debut > 0.15: bornes.append((round(debut, 2), round(a, 2)))
        debut = en[i] if i < len(en) else D
    if D - debut > 0.15: bornes.append((round(debut, 2), round(D, 2)))
    return bornes


def transcrire(wav, bornes):
    import sherpa_onnx
    r = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=ASR + 'small-encoder.int8.onnx', decoder=ASR + 'small-decoder.int8.onnx',
                                                   tokens=ASR + 'small-tokens.txt', language='fr', task='transcribe', num_threads=4)
    s, sr = sf.read(wav)
    if s.ndim > 1: s = s.mean(1)
    s16 = resample_poly(s.astype(np.float32), 16000, sr).astype(np.float32)
    res = []
    for a, b in bornes:
        x = s16[int(max(0, a - .1) * 16000):int((b + .1) * 16000)]
        t = r.create_stream(); t.accept_waveform(16000, x); r.decode_stream(t)
        res.append(t.result.text.strip())
    return res


if __name__ == '__main__':
    w = sys.argv[1]
    b = segments(w)
    for (a, z), t in zip(b, transcrire(w, b)):
        print(f'{a:6.2f}-{z:6.2f}  {t}')
    print(len(b), 'segments', ('attendus ' + sys.argv[2]) if len(sys.argv) > 2 else '')
