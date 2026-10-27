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
    vus = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n): vus.setdefault(pi[a + j], []).append(tm[b + j])
    seg = []
    for i in range(len(phrases)):
        if i in vus: seg.append([M[min(vus[i])]['debut'], M[max(vus[i])]['fin']])
        else: seg.append(None)
    # phrases non reconnues : entre la précédente et la suivante
    for i, s in enumerate(seg):
        if s is None:
            a = seg[i - 1][1] if i else 0.0
            b = next((x[0] for x in seg[i + 1:] if x), M[-1]['fin'])
            seg[i] = [a, b]
    for i in range(1, len(seg)):  # jamais de chevauchement
        if seg[i][0] < seg[i - 1][1]: seg[i][0] = seg[i - 1][1]
    return [tuple(s) for s in seg], sum(1 for i in range(len(phrases)) if i not in vus)
