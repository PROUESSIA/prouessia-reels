"""Mesure le ton d'une voix off (WAV) : débit, hauteur, énergie, pauses, attaque.

Usage : python3 moteur/analyse_voix.py NN/voix.wav [nombre_de_mots]
Sortie : un dictionnaire JSON à copier dans etat.json (champ "voix_mesures").
Uniquement numpy/scipy, aucun service en ligne.
"""
import json, sys
import numpy as np
from scipy.io import wavfile


def charger(chemin):
    import subprocess, tempfile, os
    tmp = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', chemin, '-ac', '1', '-ar', '24000', tmp], check=True)
    sr, x = wavfile.read(tmp); os.remove(tmp)
    x = x.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    m = np.abs(x).max() or 1.0
    return sr, x / m


def trames(x, sr, ms=30):
    n = int(sr * ms / 1000)
    k = len(x) // n
    return x[:k * n].reshape(k, n), ms / 1000


def f0_trame(t, sr, fmin=70, fmax=400):
    t = t - t.mean()
    ac = np.correlate(t, t, 'full')[len(t) - 1:]
    if ac[0] <= 0:
        return None
    a, b = int(sr / fmax), int(sr / fmin)
    if b >= len(ac):
        return None
    lag = a + int(np.argmax(ac[a:b]))
    return sr / lag if ac[lag] / ac[0] > 0.45 else None


def analyser(chemin, mots=None):
    sr, x = charger(chemin)
    T, dt = trames(x, sr)
    rms = np.sqrt((T ** 2).mean(axis=1)) + 1e-9
    db = 20 * np.log10(rms)
    seuil = db.max() - 35
    parle = db > seuil

    # pauses : silences d'au moins 150 ms entre deux zones parlées
    pauses, cur = [], 0
    debut = int(np.argmax(parle)); fin = len(parle) - int(np.argmax(parle[::-1]))
    for p in parle[debut:fin]:
        if not p:
            cur += 1
        else:
            if cur * dt >= 0.15:
                pauses.append(cur * dt)
            cur = 0
    duree_parole = float(parle.sum() * dt)

    f0 = [f0_trame(T[i], sr) for i in np.where(parle)[0]]
    f0 = np.array([f for f in f0 if f])
    demi_tons = 12 * np.log2(f0 / np.median(f0)) if len(f0) else np.array([0])

    db_parle = db[parle]
    une_s = int(1 / dt)
    z = db[debut:debut + une_s][parle[debut:debut + une_s]]
    attaque = float(z.mean() - db_parle.mean()) if len(z) else 0.0

    r = {
        'duree_s': round(len(x) / sr, 1),
        'parole_s': round(duree_parole, 1),
        'hauteur_moyenne_hz': round(float(np.median(f0)), 0) if len(f0) else None,
        'variation_hauteur_demi_tons': round(float(np.std(demi_tons)), 2),
        'etendue_hauteur_demi_tons': round(float(np.percentile(demi_tons, 95) - np.percentile(demi_tons, 5)), 1),
        'dynamique_db': round(float(np.percentile(db_parle, 90) - np.percentile(db_parle, 10)), 1),
        'attaque_db': round(attaque, 1),
        'pauses_n': len(pauses),
        'pause_moyenne_s': round(float(np.mean(pauses)), 2) if pauses else 0,
        'delai_premier_mot_s': round(debut * dt, 2),
    }
    if mots:
        r['debit_mots_par_s'] = round(mots / duree_parole, 2)
    return r


if __name__ == '__main__':
    mots = int(sys.argv[2]) if len(sys.argv) > 2 else None
    print(json.dumps(analyser(sys.argv[1], mots), ensure_ascii=False, indent=1))
