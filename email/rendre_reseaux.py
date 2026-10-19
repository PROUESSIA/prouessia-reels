"""Icônes réseaux pour la signature (ronds bleu nuit, pictogramme blanc) : email/reseau-instagram.png, -tiktok.png, -youtube.png (84 px, affichées en 28 px)."""
import asyncio
from playwright.async_api import async_playwright
G = {
 'instagram': '<rect x="5" y="5" width="14" height="14" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="3.2" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.3" cy="7.7" r="1" fill="#fff"/>',
 'tiktok': '<path d="M13.2 5v9.2a2.7 2.7 0 1 1-2.2-2.65" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/><path d="M13.2 5c.3 2 1.6 3.3 3.6 3.5" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/>',
 'youtube': '<rect x="4.5" y="7" width="15" height="10" rx="3" fill="#fff"/><path d="M10.6 9.6v4.8l4-2.4z" fill="#142445"/>',
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=3)
        for n, g in G.items():
            await pg.set_content(f'<body style="margin:0;background:transparent"><svg id="s" width="28" height="28" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#142445"/>{g}</svg></body>')
            await pg.locator('#s').screenshot(path=f'email/reseau-{n}.png', omit_background=True)
        await b.close()
asyncio.run(main())
