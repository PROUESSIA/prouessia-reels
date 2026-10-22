"""Signature sonore de « Sous pression » (sans musique) : la sonnerie du téléphone de Julien et le générique de fin.
Sons synthétisés ici, originaux, libres de droits. python3 sons.py → sons/sonnerie.wav, sons/generique.wav"""
import os, numpy as np, soundfile as sf
SR = 24000; D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sons'); os.makedirs(D, exist_ok=True)
t_ = lambda d: np.arange(int(d * SR)) / SR
def goutte(f0=1900, f1=700, d=.09):   # « plic » : glissando rapide comme une goutte d'eau
    t = t_(d); f = f1 + (f0 - f1) * np.exp(-t * 45); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 38) * (1 - np.exp(-t * 900))
def vibre(d=.35):                      # vibreur du téléphone posé sur la table de nuit
    t = t_(d); return (np.sign(np.sin(2 * np.pi * 145 * t)) * .5 + np.sin(2 * np.pi * 290 * t) * .3) * (.5 + .5 * np.sin(2 * np.pi * 9 * t)) * np.minimum(1, t * 40) * np.minimum(1, (d - t) * 40)
def place(buf, s, t, g=1.0):
    i = int(t * SR); buf[i:i + len(s)] += s[:max(0, len(buf) - i)] * g
# sonnerie : vibreur + motif « plic-plic… plic » (trois gouttes, la dernière plus grave), répété deux fois
son = np.zeros(int(1.7 * SR))
for k in range(2):
    b = k * .82; place(son, vibre(.34), b, .32)
    for dt, f0, f1 in ((0, 2100, 900), (.11, 2100, 900), (.30, 1500, 520)): place(son, goutte(f0, f1), b + dt, .75)
son /= np.abs(son).max() / .85; sf.write(f'{D}/sonnerie.wav', son, SR)
# générique de fin : montée de pression (souffle filtré), « clac » de vanne, puis une goutte
g = np.zeros(int(2.6 * SR)); rng = np.random.default_rng(3)
n = int(1.3 * SR); bruit = rng.normal(0, 1, n); k = np.ones(30) / 30; souffle = np.convolve(bruit, k, 'same') * np.linspace(0, 1, n) ** 2
souffle *= 1 + .4 * np.sin(2 * np.pi * np.linspace(3, 14, n) * np.linspace(0, 1.3, n)); place(g, souffle, 0, .5)
tc = t_(.18); clac = (np.sin(2 * np.pi * 160 * tc) * .8 + rng.normal(0, 1, len(tc)) * .6) * np.exp(-tc * 30); place(g, clac, 1.3, 1.0)
place(g, goutte(1700, 600, .12), 1.75, .8); place(g, goutte(1300, 450, .12), 2.05, .45)
g /= np.abs(g).max() / .85; sf.write(f'{D}/generique.wav', g, SR)
print('ok')

# fond de tension (« musique sans instrument ») : battements de cœur, tic-tac, gouttes, souffle grave — 96 BPM, 70 s
def coeur(g=1.0):
    tb = t_(.16); f = 52 + 40 * np.exp(-tb * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tb * 22); return s * g
def tic():
    tb = t_(.025); return rng.normal(0, 1, len(tb)) * np.exp(-tb * 260) * .6 + np.sin(2 * np.pi * 3200 * tb) * np.exp(-tb * 300) * .4
L = 70; fond = np.zeros(int(L * SR)); beat = 60 / 96
nb = int(L / beat)
for k in range(nb):
    tb = k * beat; mont = min(1.0, .45 + k / nb)                  # la tension monte doucement
    place(fond, coeur(1.0 * mont), tb); place(fond, coeur(.6 * mont), tb + .2)
    place(fond, tic(), tb + beat / 2, .35); place(fond, tic(), tb, .2)
    if k % 8 == 5: place(fond, goutte(1500 + 300 * (k % 3), 500, .1), tb + beat * .75, .35)
n = len(fond); br = np.cumsum(rng.normal(0, 1, n)); br -= np.convolve(br, np.ones(2400) / 2400, 'same')   # souffle grave (bruit brun)
br = br / np.abs(br).max() * (.55 + .45 * np.sin(2 * np.pi * np.arange(n) / SR / 7.5)); fond += br * .35
fond /= np.abs(fond).max() / .8; sf.write(f'{D}/tension.wav', fond, SR)
print('tension ok')
