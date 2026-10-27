"""Calage par les mots : voix/transcrire/<nom>.json (mots horodatés, Action « Transcrire ») → (début, fin) par phrase."""
import json, re, unicodedata, difflib
def norm(t):
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = t.replace('prouessia', 'prouessia').replace('pouessia', 'prouessia')
    return re.findall(r"[a-z0-9]+", t)
def caler(fichier_mots, phrases):
    M = json.load(open(fichier_mots))
    tw, tm = [], []
    for k, m in enumerate(M):
        for x in norm(m['mot']): tw.append(x); tm.append(k)
    pw, pi = [], []
    for i, p in enumerate(phrases):
        for x in norm(p): pw.append(x); pi.append(i)
    sm = difflib.SequenceMatcher(None, pw, tw, autojunk=False)
    vus = {}; pt = {}   # pt : jeton de phrase → mot transcrit
    for a, b, n in sm.get_matching_blocks():
        for j in range(n): vus.setdefault(pi[a + j], []).append(tm[b + j]); pt[a + j] = tm[b + j]
    prem = {i: pi.index(i) for i in set(pi)}; dern = {i: len(pi) - 1 - pi[::-1].index(i) for i in set(pi)}
    seg = []
    for i in range(len(phrases)):
        if i not in vus: seg.append(None); continue
        k0, k1 = min(vus[i]), max(vus[i])
        if prem[i] not in pt:   # début non reconnu (chiffres, noms) : on reprend les mots transcrits juste avant
            avant = max([max(vus[j]) for j in vus if j < i], default=-1); k0 = avant + 1
        if dern[i] not in pt:
            apres = min([min(vus[j]) for j in vus if j > i], default=len(M)); k1 = apres - 1
        seg.append([M[k0]['debut'], M[k1]['fin']])
    # phrases non reconnues : entre la précédente et la suivante
    for i, s in enumerate(seg):
        if s is None:
            a = seg[i - 1][1] if i else 0.0
            b = next((x[0] for x in seg[i + 1:] if x), M[-1]['fin'])
            seg[i] = [a, b]
    for i in range(1, len(seg)):  # jamais de chevauchement
        if seg[i][0] < seg[i - 1][1]: seg[i][0] = seg[i - 1][1]
    return [tuple(s) for s in seg], sum(1 for i in range(len(phrases)) if i not in vus)
