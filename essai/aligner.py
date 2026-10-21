"""Aligne une voix (wav) sur une liste de phrases : découpe aux silences puis programmation dynamique sur le nombre de syllabes.
Sortie : liste (début, fin) par phrase."""
import re, subprocess, sys
def silences(wav, seuil=-35, d=0.1):
    o = subprocess.run(['ffmpeg', '-i', wav, '-af', f'silencedetect=n={seuil}dB:d={d}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]; e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
    return list(zip(s, e + [dur][:len(s) - len(e)])), dur
def syll(t):
    t = re.sub(r'<[^>]+>|&nbsp;', ' ', t).lower()
    return max(1, len(re.findall(r'[aeiouyàâéèêëîïôûùü]+', t)))
def aligner(wav, phrases):
    sil, dur = silences(wav)
    # morceaux de parole entre les silences
    bornes = [0.0]; fins = []
    morceaux = []; t = 0.0
    for a, b in sil:
        if a - t > 0.05: morceaux.append((t, a))
        t = b
    if dur - t > 0.05: morceaux.append((t, dur))
    n, m = len(phrases), len(morceaux)
    S = [syll(p) for p in phrases]; k = sum(b - a for a, b in morceaux) / sum(S)
    INF = 1e9; C = [[INF] * (m + 1) for _ in range(n + 1)]; P = [[0] * (m + 1) for _ in range(n + 1)]; C[0][0] = 0
    for i in range(1, n + 1):
        for j in range(i, m + 1):
            for q in range(i - 1, j):
                g = morceaux[q:j]; parole = sum(b - a for a, b in g)
                trous = sum(g[x + 1][0] - g[x][1] for x in range(len(g) - 1))
                c = C[i - 1][q] + (parole - k * S[i - 1]) ** 2 + 2 * trous ** 2
                if c < C[i][j]: C[i][j] = c; P[i][j] = q
    res = []; j = m
    for i in range(n, 0, -1):
        q = P[i][j]; res.append((morceaux[q][0], morceaux[j - 1][1])); j = q
    return res[::-1]
