// Prouessia · STYLE 5 « motion » (validé par la fondatrice le 30/10/2026 sur l'essai « La relance part toute seule »).
// Film générique piloté par script.json (scènes) + timing.json (début/fin de chaque phrase dite).
// Pure function of time: window.seek(t) paints frame t. 1 beat = 1 s. AUCUNE musique (voix seule).
//
// Scènes possibles (script.json → phrases[i].scene) :
//   texte     { fond: 'ink'|'accent', lignes: [...], jaune: [index des lignes en jaune], badge: ['LUN.', '26'] (option), bulle: true (option : « … » qui tape) }
//   surligne  { fond, ligne: 'Relancer ?', surligne: 'Ça vous gêne.' }   (la 2e ligne arrive dans un bandeau jaune)
//   app       { haut: ['ligne blanche', 'ligne jaune'], capture: 'nom d'une image de videos/app (ex. extras/14-reglage-relance)', pastille: 'Activée ✓' (option) }
//             (les scènes app qui se suivent forment un carrousel de vrais écrans)
//   question  { lignes: [...] }   (fond jaune, grand « ? »)
//   fin       {}                  (logo, « Le partenaire des plombiers », puis l'appel DEVIS si script.cta !== false)
import * as M from './lib/motion.js';

const { W, H, FORMAT, E, prog, springU, SPRING, wobble, font, layout, glyph, text, fill, rrect, clamp, shake } = M;
const C = { ink: '#0B1B3A', paper: '#F7F5EF', accent: '#F2B705', mute: '#8A93A6', white: '#FFFFFF' };
const DISPLAY = 'Display', UI = 'UI';
let S = null, T = null, CTA = null, uNow = 0, ctx0 = null;

function kinetic(ctx, str, x, base, size, color, u0, { stagger = 0.022, from = 140, exitAt = null } = {}) {
  const f = font(size, 900, DISPLAY), L = layout(ctx, str, f, -0.03 * size);
  L.glyphs.forEach((g, j) => {
    const k = springU(uNow, u0 + j * stagger, SPRING.bouncy);
    if (k <= 0) return;
    let dy = (1 - k) * from;
    if (exitAt !== null) dy -= E.inBack(prog(uNow, exitAt + j * 0.01, exitAt + 0.35 + j * 0.01), 1.6) * (H * 0.7);
    glyph(ctx, g.ch, x + g.cx, base + dy, f, color, k, k);
  });
  return L;
}
// la plus grande taille qui fait tenir toutes les lignes dans la largeur utile
function fit(ctx, lignes, max, min = 70) {
  const wmax = FORMAT.safe.w - 10;
  let size = max;
  for (; size > min; size -= 4) {
    const f = font(size, 900, DISPLAY);
    if (lignes.every((l) => layout(ctx, l, f, -0.03 * size).width <= wmax)) break;
  }
  return size;
}
function phone(ctx, img, cx, cy, w, { fy = 0, rot = 0, scale = 1 } = {}) {
  const h = w * 2532 / 1170 * 0.70;
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(scale, scale);
  ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 60; ctx.shadowOffsetY = 30;
  rrect(ctx, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 54); ctx.fillStyle = '#111'; ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.save(); rrect(ctx, -w / 2, -h / 2, w, h, 42); ctx.clip();
  const sh = img.width * h / w, sy = clamp(fy, 0, 1) * (img.height - sh);
  ctx.drawImage(img, 0, sy, img.width, sh, -w / 2, -h / 2, w, h);
  ctx.restore(); ctx.restore();
}

// ------------------------------------------------------------------ scènes
function sTexte(ctx, u, i, ph) {
  const bg = ph.fond === 'accent' ? C.accent : C.ink, fg = ph.fond === 'accent' ? C.ink : C.white;
  fill(ctx, bg);
  const s = FORMAT.safe, a = T[i].a, b = T[i].b, L = ph.lignes || [];
  const size = fit(ctx, L, ph.taille || 210), lh = size * 1.04;
  const top = H * 0.5 - (L.length * lh) / 2 + size * 0.8 + (ph.badge ? 120 : 0);
  if (ph.badge) {
    const k = springU(u, a - 0.5, SPRING.bouncy);
    if (k > 0) {
      ctx.save(); ctx.translate(s.x + 140, top - size - 220); ctx.rotate(-0.04 - 0.08 * (1 - k)); ctx.scale(k, k);
      rrect(ctx, -130, -130, 260, 260, 40); ctx.fillStyle = ph.fond === 'accent' ? C.ink : C.paper; ctx.fill();
      ctx.fillStyle = C.accent; ctx.beginPath(); ctx.roundRect(-130, -130, 260, 72, [40, 40, 0, 0]); ctx.fill();
      text(ctx, ph.badge[0], 0, -78, font(48, 900, DISPLAY), C.ink, 'center');
      text(ctx, ph.badge[1], 0, 80, font(140, 900, DISPLAY), ph.fond === 'accent' ? C.white : C.ink, 'center');
      ctx.restore();
    }
  }
  const nextA = T[i + 1] ? T[i + 1].a : b + 1;
  L.forEach((l, j) => {
    const jaune = (ph.jaune || []).includes(j);
    kinetic(ctx, l, s.x, top + j * lh, size, jaune ? (ph.fond === 'accent' ? C.white : C.accent) : fg, a + j * 0.22,
      { from: j === 0 ? 220 : 140, exitAt: j === L.length - 1 ? nextA - 0.3 : null });
  });
  if (ph.bulle) {
    const k = springU(u, a + 0.2, SPRING.gentle), gone = E.inCubic(prog(u, b - 0.6, b - 0.2));
    if (k > 0 && gone < 1) {
      ctx.save(); ctx.translate(W - s.x - 165, Math.min(H * 0.8, top + L.length * lh + 120)); ctx.scale(k * (1 - gone), k * (1 - gone));
      rrect(ctx, -165, -70, 330, 140, 70); ctx.fillStyle = ph.fond === 'accent' ? C.ink : C.accent; ctx.fill();
      for (let d = 0; d < 3; d++) {
        ctx.beginPath(); ctx.arc(-70 + d * 70, Math.sin((u - a) * 9 - d * 0.9) * 10, 18, 0, M.TAU); ctx.fillStyle = C.paper; ctx.fill();
      }
      ctx.restore();
    }
  }
}
function sSurligne(ctx, u, i, ph) {
  const accent = ph.fond === 'accent';
  fill(ctx, accent ? C.accent : C.ink);
  const s = FORMAT.safe, a = T[i].a;
  const size = fit(ctx, [ph.ligne], 190), size2 = fit(ctx, [ph.surligne], 150) - 8;
  const y0 = H * 0.45;
  ctx.save(); shake(ctx, u, a + 0.3, 7, 5, 0.6);
  kinetic(ctx, ph.ligne, s.x, y0, size, accent ? C.ink : C.white, a);
  ctx.restore();
  const k = springU(u, a + 0.7, SPRING.snappy);
  if (k > 0) {
    const f = font(size2, 900, DISPLAY), L = layout(ctx, ph.surligne, f, -4), y = y0 + size * 0.5 + size2 * 1.1;
    ctx.save(); ctx.beginPath(); ctx.rect(s.x - 20, y - size2 * 1.02, (L.width + 50) * k, size2 * 1.36);
    ctx.fillStyle = accent ? C.ink : C.accent; ctx.fill(); ctx.restore();
    if (k > 0.5) text(ctx, ph.surligne, s.x + 10, y, f, accent ? C.accent : C.ink, 'left', -4);
  }
}
function sApp(ctx, u, i, IMG) {
  fill(ctx, C.paper);
  const s = FORMAT.safe;
  let g0 = i; while (g0 > 0 && S.phrases[g0 - 1].scene === 'app') g0--;
  let g1 = i; while (g1 + 1 < S.phrases.length && S.phrases[g1 + 1].scene === 'app') g1++;
  const ph = S.phrases[i], a0 = T[g0].a;
  ctx.fillStyle = C.ink; ctx.fillRect(0, 0, W, H * 0.30);
  const haut = ph.haut || [];
  const hs = fit(ctx, haut, 112, 64);
  if (haut[0]) kinetic(ctx, haut[0], s.x, H * 0.145, hs, C.white, T[i].a - 0.05, { stagger: 0.015, from: 90 });
  if (haut[1]) kinetic(ctx, haut[1], s.x, H * 0.145 + hs * 1.07, hs, C.accent, T[i].a + 0.12, { stagger: 0.015, from: 90 });
  const enter = springU(u, a0 - 0.1, SPRING.gentle), w = 720, cy = H * 0.665;
  let shift = 0; for (let k = g0 + 1; k <= g1; k++) shift += springU(u, T[k].a - 0.1, SPRING.snappy);
  for (let k = g0; k <= g1; k++) {
    const img = IMG['cap' + k]; if (!img) continue;
    const n = k - g0, x = W / 2 + (n - shift) * (w + 140);
    if (x < -w || x > W + w) continue;
    phone(ctx, img, x, cy + (1 - enter) * H * 0.8, w, { fy: (u - a0) * 0.004, rot: (n - shift) * 0.05, scale: 1 - 0.06 * Math.min(1, Math.abs(n - shift)) });
  }
  if (ph.pastille) {
    const nextA = T[i + 1] ? T[i + 1].a : T[i].b + 1;
    const pk = springU(u, T[i].a + 0.6, SPRING.bouncy) * (1 - prog(u, nextA - 0.2, nextA));
    if (pk > 0) {
      ctx.save(); ctx.translate(W / 2 + 230, cy - 360); ctx.rotate(0.12); ctx.scale(pk, pk);
      const f = font(50, 900, DISPLAY); ctx.font = f; const tw = ctx.measureText(ph.pastille).width + 90;
      rrect(ctx, -tw / 2, -52, tw, 104, 52); ctx.fillStyle = C.accent; ctx.fill();
      text(ctx, ph.pastille, 0, 18, f, C.ink, 'center');
      ctx.restore();
    }
  }
}
function sQuestion(ctx, u, i, ph) {
  fill(ctx, C.accent);
  const s = FORMAT.safe, a = T[i].a, L = ph.lignes || [];
  const size = fit(ctx, L, 175), lh = size * 1.08, top = H * 0.42 - (L.length * lh) / 2 + size * 0.8;
  L.forEach((l, j) => kinetic(ctx, l, s.x, top + j * lh, size, C.ink, a + j * 0.18));
  const q = springU(u, a + 0.9, SPRING.bouncy);
  if (q > 0) {
    ctx.save(); ctx.translate(W - s.x - 130, Math.min(H * 0.86, top + L.length * lh + 260)); ctx.rotate(0.15 + 0.1 * wobble(u - a - 0.9, 2, 4)); ctx.scale(q, q);
    text(ctx, '?', 0, 0, font(420, 900, DISPLAY), C.ink, 'center');
    ctx.restore();
  }
}
function sFin(ctx, u, i, IMG) {
  fill(ctx, C.ink);
  const s = FORMAT.safe, a = T[i].a;
  const k = springU(u, a - 0.1, SPRING.bouncy), ly = s.y + 120;
  if (IMG.logo && k > 0) {
    ctx.save(); ctx.translate(s.x + 70, ly); ctx.scale(k, k); ctx.rotate(-0.3 * (1 - k));
    ctx.save(); rrect(ctx, -70, -70, 140, 140, 32); ctx.clip(); ctx.drawImage(IMG.logo, -70, -70, 140, 140); ctx.restore();
    ctx.restore();
    text(ctx, 'prouessia', s.x + 170, ly + 22, font(64, 900, DISPLAY), C.white);
  }
  kinetic(ctx, 'Le partenaire', s.x, H * 0.45, 120, C.white, a + 0.2);
  kinetic(ctx, 'des plombiers', s.x, H * 0.45 + 135, 120, C.accent, a + 0.45);
  if (!CTA) text(ctx, 'prouessia.fr', W / 2, H - s.y * 0.5 - 40, font(46, 700, UI), C.mute, 'center');
}
// plan à part pour la phrase d'appel (décision de la fondatrice, 30/10) : fond jaune, appel DEVIS, prouessia.fr en bas
function sCta(ctx, u, IMG) {
  fill(ctx, C.accent);
  const s = FORMAT.safe, a = CTA.a;
  const k = springU(u, a - 0.1, SPRING.bouncy);
  if (IMG.logo && k > 0) {
    ctx.save(); ctx.translate(W / 2 - 150, s.y + 120); ctx.scale(k, k);
    ctx.save(); rrect(ctx, -60, -60, 120, 120, 28); ctx.clip(); ctx.drawImage(IMG.logo, -60, -60, 120, 120); ctx.restore();
    ctx.restore();
    ctx.globalAlpha = Math.min(1, k); text(ctx, 'prouessia', W / 2 - 70, s.y + 142, font(60, 900, DISPLAY), C.ink); ctx.globalAlpha = 1;
  }
  const z = fit(ctx, ['Vous voulez', 'en savoir plus ?', 'en commentaire'], 120);
  kinetic(ctx, 'Vous voulez', s.x, H * 0.36, z, C.ink, a);
  kinetic(ctx, 'en savoir plus ?', s.x, H * 0.36 + z * 1.08, z, C.ink, a + 0.2);
  kinetic(ctx, 'Écrivez', s.x, H * 0.36 + 330, 130, C.ink, a + 0.6);
  const kd = springU(u, a + 0.9, SPRING.bouncy);
  if (kd > 0) {
    const fW = font(130, 900, DISPLAY);
    ctx.save(); ctx.translate(s.x + 230, H * 0.36 + 500); ctx.rotate(-0.04); ctx.scale(kd, kd);
    rrect(ctx, -230, -110, 460, 160, 30); ctx.fillStyle = C.ink; ctx.fill();
    text(ctx, S.mot || 'DEVIS', 0, 28, fW, C.accent, 'center');
    ctx.restore();
  }
  kinetic(ctx, 'en commentaire', s.x, H * 0.36 + 680, z, C.ink, a + 1.1);
  const ks = springU(u, a + 1.3, SPRING.gentle);
  if (ks > 0) { ctx.globalAlpha = Math.min(1, ks); text(ctx, 'prouessia.fr', W / 2, H - s.y * 0.5 - 40 + (1 - ks) * 80, font(64, 900, DISPLAY), C.ink, 'center'); ctx.globalAlpha = 1; }
}

M.film({
  fonts: [font(100, 900, DISPLAY), font(40, 700, UI)],
  images: (() => ({ logo: 'assets/logo.png' }))(),
  hits: [],
  samples: 8,
  async init(ctx, IMG) {
    S = await fetch('script.json').then((r) => r.json());
    const tj = await fetch('timing.json').then((r) => r.json());
    T = tj.phrases; CTA = tj.cta || null;
    // captures des scènes app (chargées ici : la liste dépend du script)
    await Promise.all(S.phrases.map(async (ph, i) => {
      if (ph.scene !== 'app') return;
      const im = new Image(); im.src = `assets/cap${i}.png`;
      try { await im.decode(); IMG['cap' + i] = im; } catch { console.error('capture manquante', i); }
    }));
  },
  draw(ctx, u, t, IMG) {
    uNow = u;
    let i = 0;
    for (let k = 0; k < T.length; k++) if (u >= T[k].a - (k ? 0.08 : 99)) i = k;
    const ph = S.phrases[i];
    if (CTA && u >= CTA.a - 0.08) sCta(ctx, u, IMG);
    else if (ph.scene === 'texte') sTexte(ctx, u, i, ph);
    else if (ph.scene === 'surligne') sSurligne(ctx, u, i, ph);
    else if (ph.scene === 'app') sApp(ctx, u, i, IMG);
    else if (ph.scene === 'question') sQuestion(ctx, u, i, ph);
    else sFin(ctx, u, i, IMG);
  },
});
