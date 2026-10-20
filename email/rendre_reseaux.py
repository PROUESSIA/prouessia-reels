"""Icônes réseaux pour la signature (ronds bleu nuit, pictogramme blanc) : email/reseau-instagram.png, -tiktok.png, -youtube.png (84 px, affichées en 28 px)."""
import asyncio
from playwright.async_api import async_playwright
G = {
 'instagram': '<rect x="5" y="5" width="14" height="14" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="3.2" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.3" cy="7.7" r="1" fill="#fff"/>',
 'tiktok': '<path d="M13.2 5v9.2a2.7 2.7 0 1 1-2.2-2.65" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/><path d="M13.2 5c.3 2 1.6 3.3 3.6 3.5" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/>',
 'facebook': '<path d="M13.3 19v-6.2h2.1l.3-2.4h-2.4V8.9c0-.7.2-1.2 1.2-1.2h1.3V5.6c-.2 0-1-.1-1.9-.1-1.9 0-3.2 1.2-3.2 3.3v1.8H8.6v2.4h2.1V19z" fill="#fff"/>',
 'linkedin': '<rect x="7" y="10.2" width="2.3" height="7" fill="#fff"/><circle cx="8.15" cy="7.4" r="1.35" fill="#fff"/><path d="M11.3 10.2h2.2v1c.4-.7 1.3-1.2 2.4-1.2 2 0 2.6 1.3 2.6 3.1v4.1h-2.3v-3.6c0-.9-.2-1.6-1.1-1.6s-1.5.6-1.5 1.6v3.6h-2.3z" fill="#fff"/>',
 'youtube':'<rect x="4.5" y="7" width="15" height="10" rx="3" fill="#fff"/><path d="M10.6 9.6v4.8l4-2.4z" fill="#142445"/>',
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=3)
        for n, g in G.items():
            await pg.set_content(f'<body style="margin:0;background:transparent"><svg id="s" width="28" height="28" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#142445"/>{g}</svg></body>')
            await pg.locator('#s').screenshot(path=f'email/reseau-{n}.png', omit_background=True)
        await b.close()
asyncio.run(main())
