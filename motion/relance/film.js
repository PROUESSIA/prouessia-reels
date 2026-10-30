// Prouessia · « La relance part toute seule » — 9:16, voix Charon, AUCUNE musique (règle de la fondatrice).
// Pure function of time: window.seek(t) paints frame t. Grid = 1 beat par seconde (u = t).
// Les débuts/fins de phrases viennent de timing.json (calage mot à mot de la voix).
import * as M from './lib/motion.js';

const { W, H, FORMAT, E, prog, lerp, springU, SPRING, wobble, font, layout, glyph, text, fill, cover, rrect, clamp, shake } = M;

// Marque Prouessia : marine, jaune, papier. Une seule couleur d'accent : le jaune.
const C = { ink: '#0B1B3A', paper: '#F7F5EF', accent: '#F2B705', mute: '#8A93A6', white: '#FFFFFF' };
const DISPLAY = 'Display', UI = 'UI';
let T = null;           // [{a, b, text}] par phrase
const P = (i) => T[i];  // phrase i

// --------------------------------------------------------------- helpers
// texte qui arrive lettre par lettre par le bas, en ressort (jamais un simple fondu)
function kinetic(ctx, str, x, base, size, color, u0, { weight = 900, family = DISPLAY, stagger = 0.022, from = 140, exitAt = null, hl = null } = {}) {
  const f = font(size, weight, family), L = layout(ctx, str, f, -0.03 * size);
  L.glyphs.forEach((g, j) => {
    const kk = springU(uNow, u0 + j * stagger, SPRING.bouncy);
    if (kk <= 0) return;
    let dy = (1 - kk) * from;
    if (exitAt !== null) dy -= E.inBack(prog(uNow, exitAt + j * 0.01, exitAt + 0.35 + j * 0.01), 1.6) * (H * 0.7);
    glyph(ctx, g.ch, x + g.cx, base + dy, f, hl && hl(j, g.ch) ? C.accent : color, kk, kk);
  });
  return L;
}
let uNow = 0;

// carte téléphone : la vraie capture, à sa taille (pas d'agrandissement : image nette)
function phone(ctx, img, cx, cy, w, { fy = 0, rot = 0, scale = 1 } = {}) {
  const h = w * 2532 / 1170 * 0.70;            // on montre le haut de l'écran (62 %) : lisible
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(scale, scale);
  ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 60; ctx.shadowOffsetY = 30;
  rrect(ctx, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 54); ctx.fillStyle = '#111'; ctx.fill();
  ctx.shadowColor = 'transparent';
  const ih = img.height * (h / (w * 2532 / 1170)) ;
  ctx.save(); rrect(ctx, -w / 2, -h / 2, w, h, 42); ctx.clip();
  const sh = img.width * h / w;                   // hauteur source visible
  const sy = clamp(fy, 0, 1) * (img.height - sh);
  ctx.drawImage(img, 0, sy, img.width, sh, -w / 2, -h / 2, w, h);
  ctx.restore(); ctx.restore();
  return h;
}

// --------------------------------------------------------------- scènes
// S1 « Le devis est parti lundi. »  marine, chip calendrier « LUN. » qui claque
function s1(ctx, u) {
  fill(ctx, C.ink);
  const s = FORMAT.safe, a = P(0).a;
  const chipK = springU(u, a - 0.5, SPRING.bouncy);
  if (chipK > 0) {
    ctx.save(); ctx.translate(s.x + 150, H * 0.24); ctx.rotate(-0.08 * (1 - chipK) - 0.04); ctx.scale(chipK, chipK);
    rrect(ctx, -130, -130, 260, 260, 40); ctx.fillStyle = C.paper; ctx.fill();
    ctx.fillStyle = C.accent; ctx.beginPath(); ctx.roundRect(-130, -130, 260, 72, [40, 40, 0, 0]); ctx.fill();
    text(ctx, 'LUN.', 0, -78, font(48, 900, DISPLAY), C.ink, 'center');
    text(ctx, '26', 0, 80, font(140, 900, DISPLAY), C.ink, 'center');
    ctx.restore();
  }
  kinetic(ctx, 'Le devis', s.x, H * 0.47, 200, C.white, a);
  kinetic(ctx, 'est parti', s.x, H * 0.47 + 210, 200, C.white, a + 0.25);
  kinetic(ctx, 'lundi.', s.x, H * 0.47 + 420, 200, C.accent, a + 0.5, { exitAt: P(1).a - 0.3 });
}

// S2 « Jeudi, toujours rien. »  jaune, bulle de messagerie vide qui « tape » puis s'arrête
function s2(ctx, u) {
  fill(ctx, C.accent);
  const s = FORMAT.safe, a = P(1).a, b = P(1).b;
  kinetic(ctx, 'Jeudi,', s.x, H * 0.33, 270, C.ink, a, { from: 260 });
  kinetic(ctx, 'toujours', s.x, H * 0.33 + 250, 200, C.ink, a + 0.35);
  kinetic(ctx, 'rien.', s.x, H * 0.33 + 460, 200, C.ink, a + 0.55);
  // bulle « … » qui apparaît puis s'efface : le client ne répond pas
  const k = springU(u, a + 0.2, SPRING.gentle), gone = E.inCubic(prog(u, b - 0.6, b - 0.2));
  if (k > 0 && gone < 1) {
    const x = W - s.x - 330, y = H * 0.74;
    ctx.save(); ctx.translate(x + 165, y); ctx.scale(k * (1 - gone), k * (1 - gone));
    rrect(ctx, -165, -70, 330, 140, 70); ctx.fillStyle = C.ink; ctx.fill();
    for (let i = 0; i < 3; i++) {
      const bob = Math.sin((u - a) * 9 - i * 0.9) * 10;
      ctx.beginPath(); ctx.arc(-70 + i * 70, bob, 18, 0, M.TAU); ctx.fillStyle = C.paper; ctx.fill();
    }
    ctx.restore();
  }
}

// S3 « Relancer ? Ça vous gêne. »  marine ; « Relancer ? » hésite (petit tremblement)
function s3(ctx, u) {
  fill(ctx, C.ink);
  const s = FORMAT.safe, a = P(2).a;
  ctx.save(); shake(ctx, u, a + 0.3, 7, 5, 0.6);
  kinetic(ctx, 'Relancer ?', s.x, H * 0.45, 190, C.white, a);
  ctx.restore();
  const k = springU(u, a + 0.7, SPRING.snappy);
  if (k > 0) {
    const f = font(132, 900, DISPLAY), L = layout(ctx, 'Ça vous gêne.', f, -4);
    const y = H * 0.45 + 230;
    ctx.save(); ctx.beginPath(); ctx.rect(s.x - 20, y - 135, (L.width + 50) * k, 180); ctx.fillStyle = C.accent; ctx.fill(); ctx.restore();
    if (k > 0.5) text(ctx, 'Ça vous gêne.', s.x + 10, y, f, C.ink, 'left', -4);
  }
}

// S4-S6 l'application : la carte téléphone glisse d'une capture à l'autre (vrais écrans)
function sApp(ctx, u, IMG) {
  fill(ctx, C.paper);
  const s = FORMAT.safe, a4 = P(3).a, a5 = P(4).a, a6 = P(5).a, b6 = P(5).b;
  // bandeau marine en haut avec la phrase dite
  const lines = [[a4, 'La relance', 'part toute seule'], [a5, 'Par e-mail,', 'à la date prévue'], [a6, 'Même sur', 'le chantier']];
  ctx.fillStyle = C.ink; ctx.fillRect(0, 0, W, H * 0.30);
  const cur = u < a5 ? 0 : u < a6 ? 1 : 2;
  const [la, l1, l2] = lines[cur];
  kinetic(ctx, l1, s.x, H * 0.145, 112, C.white, la - 0.05, { stagger: 0.015, from: 90 });
  kinetic(ctx, l2, s.x, H * 0.145 + 120, 112, C.accent, la + 0.12, { stagger: 0.015, from: 90 });
  // la carte : arrive par le bas, puis glisse latéralement (whip à deux écrans visibles)
  const enter = springU(u, a4 - 0.1, SPRING.gentle);
  const shots = [IMG.reglage, IMG.suivi, IMG.mail];
  const w = 720, cy = H * 0.665;
  const pos = [springU(u, a5 - 0.1, SPRING.snappy), springU(u, a6 - 0.1, SPRING.snappy)];
  const shift = pos[0] + pos[1];                       // 0 → 1 → 2
  const fy = [0, 0.02, 0.05];
  shots.forEach((img, i) => {
    if (!img) return;
    const x = W / 2 + (i - shift) * (w + 140);
    if (x < -w || x > W + w) return;
    const y = cy + (1 - enter) * H * 0.8;
    const sc = 1 - 0.06 * Math.min(1, Math.abs(i - shift));
    const drift = (u - a4) * 0.004;                    // lente descente dans l'écran : ça vit
    phone(ctx, img, x, y, w, { fy: fy[i] + drift, rot: (i - shift) * 0.05, scale: sc });
  });
  // pastille « Activée » qui claque sur le premier écran
  const pk = springU(u, a4 + 0.6, SPRING.bouncy) * (1 - prog(u, a5 - 0.2, a5));
  if (pk > 0) {
    ctx.save(); ctx.translate(W / 2 + 230, cy - 360); ctx.rotate(0.12); ctx.scale(pk, pk);
    rrect(ctx, -150, -52, 300, 104, 52); ctx.fillStyle = C.accent; ctx.fill();
    text(ctx, 'Activée ✓', 0, 18, font(50, 900, DISPLAY), C.ink, 'center');
    ctx.restore();
  }
}

// S7 « Et vous, vous relancez vos devis ? »  jaune, question qui monte
function s7(ctx, u) {
  fill(ctx, C.accent);
  const s = FORMAT.safe, a = P(6).a;
  kinetic(ctx, 'Et vous,', s.x, H * 0.30, 170, C.ink, a);
  kinetic(ctx, 'vous', s.x, H * 0.30 + 185, 170, C.ink, a + 0.25);
  kinetic(ctx, 'relancez', s.x, H * 0.30 + 370, 170, C.ink, a + 0.4);
  kinetic(ctx, 'vos devis ?', s.x, H * 0.30 + 555, 170, C.ink, a + 0.55);
  const q = springU(u, a + 0.9, SPRING.bouncy);
  if (q > 0) {
    ctx.save(); ctx.translate(W - s.x - 130, H * 0.82); ctx.rotate(0.15 + 0.1 * wobble(u - a - 0.9, 2, 4)); ctx.scale(q, q);
    text(ctx, '?', 0, 0, font(420, 900, DISPLAY), C.ink, 'center');
    ctx.restore();
  }
}

// S8-S9 fin : logo, « le partenaire des plombiers », puis l'appel DEVIS
function sEnd(ctx, u, IMG) {
  fill(ctx, C.ink);
  const s = FORMAT.safe, a = P(7).a, c = T.cta;
  const k = springU(u, a - 0.1, SPRING.bouncy);
  const ly = s.y + 120;
  if (IMG.logo && k > 0) {
    ctx.save(); ctx.translate(s.x + 70, ly); ctx.scale(k, k); ctx.rotate(-0.3 * (1 - k));
    ctx.save(); rrect(ctx, -70, -70, 140, 140, 32); ctx.clip(); ctx.drawImage(IMG.logo, -70, -70, 140, 140); ctx.restore();
    ctx.restore();
    text(ctx, 'prouessia', s.x + 170, ly + 22, font(64, 900, DISPLAY), C.white);
  }
  const ty = ly + 330;
  kinetic(ctx, 'Le partenaire', s.x, ty, 120, C.white, a + 0.2);
  kinetic(ctx, 'des plombiers', s.x, ty + 135, 120, C.accent, a + 0.45);
  const k2 = springU(u, c.a - 0.1, SPRING.snappy);
  const by = ty + 300;
  if (k2 > 0) {
    const y = by + (1 - k2) * 260, bw = W - 2 * s.x;
    ctx.save(); ctx.globalAlpha = Math.min(1, k2 * 1.5);
    rrect(ctx, s.x - 10, y, bw + 20, 470, 44); ctx.fillStyle = C.paper; ctx.fill();
    text(ctx, 'Vous voulez en savoir plus ?', s.x + 40, y + 95, font(54, 800, UI), C.ink);
    const fW = font(100, 900, DISPLAY);
    text(ctx, 'Écrivez', s.x + 40, y + 235, fW, C.ink);
    ctx.font = fW; const ew = ctx.measureText('Écrivez').width;
    const kd = springU(u, c.a + 0.9, SPRING.bouncy);
    if (kd > 0) {
      const px = s.x + 40 + ew + 40 + 190;
      ctx.save(); ctx.translate(px, y + 200); ctx.rotate(-0.05); ctx.scale(kd, kd);
      rrect(ctx, -190, -78, 380, 135, 26); ctx.fillStyle = C.accent; ctx.fill();
      text(ctx, 'DEVIS', 0, 34, fW, C.ink, 'center');
      ctx.restore();
    }
    text(ctx, 'en commentaire', s.x + 40, y + 380, font(84, 900, DISPLAY), C.ink);
    ctx.restore();
  }
  text(ctx, 'prouessia.fr', W / 2, H - s.y * 0.5 - 40, font(46, 700, UI), C.mute, 'center');
}

M.film({
  fonts: [font(100, 900, DISPLAY), font(40, 700, UI)],
  images: { reglage: 'assets/shots/reglage.png', suivi: 'assets/shots/suivi.png', mail: 'assets/shots/mail.png', logo: 'assets/logo.png' },
  hits: [],
  samples: 8,
  async init() { const j = await fetch('timing.json').then((r) => r.json()); T = j.phrases; T.cta = j.cta; },
  draw(ctx, u, t, IMG) {
    uNow = u;
    if (u < P(1).a - 0.05) s1(ctx, u);
    else if (u < P(2).a - 0.05) s2(ctx, u);
    else if (u < P(3).a - 0.12) s3(ctx, u);
    else if (u < P(6).a - 0.05) sApp(ctx, u, IMG);
    else if (u < P(7).a - 0.12) s7(ctx, u);
    else sEnd(ctx, u, IMG);
  },
});
