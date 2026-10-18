"""Dump computed styles and boxes of key swift.org home elements at 1280px (light and dark)."""
import json
from playwright.sync_api import sync_playwright
SEL = {
 "nav": ".site-navigation", "nav-item": ".desktop-navigation .nav-item a > span", "logo": ".site-navigation .logo a",
 "hero-section": "#what-is-swift", "title-0": "#what-is-swift h1", "sub-text": "#what-is-swift .sub-text h2",
 "install-btn": "#what-is-swift .hero-content > a", "install-caption": "#what-is-swift .hero-content > p",
 "create-h2": "#what-is-swift .hero-content > h2", "primary-card": "ul.primary-links li a", "primary-icon": "ul.primary-links li a i",
 "primary-title": "ul.primary-links .title", "primary-sub": "ul.primary-links .subtitle", "secondary-card": "ul.secondary-links li a",
 "secondary-title": "ul.secondary-links .title", "pillar-1": "#pillar-1", "pillar-intro": ".pillar-intro",
 "callout": "#pillar-1 .callout", "callout-text-col": "#pillar-1 .callout .text", "callout-code-col": "#pillar-1 .callout .code",
 "callout-title": "#pillar-1 .callout-title", "callout-subtitle": "#pillar-1 .callout-subtitle", "callout-body": "#pillar-1 .callout-text",
 "pre": "#pillar-1 pre.highlight", "code": "#pillar-1 pre.highlight code", "pillar-2": "#pillar-2", "pillar-3": "#pillar-3",
 "os-title": "#pillar-3 .callout-title", "os-sub": "#pillar-3 .callout-subtitle", "os-link": "#pillar-3 .links a",
 "footer": "footer.global-footer", "footer-h3": "footer.global-footer h3", "footer-link": "footer.global-footer nav ul li a",
}
PROPS = ["font-family","font-size","font-weight","line-height","letter-spacing","color","background-color","background-image",
         "padding","margin","border","border-radius","box-shadow","max-width","text-align","opacity"]
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for scheme in ("light","dark"):
        pg = b.new_context(viewport={"width":1280,"height":900}, color_scheme=scheme).new_page()
        pg.goto("https://www.swift.org/", wait_until="networkidle")
        out[scheme] = pg.evaluate("""([sel, props]) => { const r = {}; for (const [k, s] of Object.entries(sel)) {
            const e = document.querySelector(s); if (!e) { r[k] = null; continue; }
            const cs = getComputedStyle(e), bb = e.getBoundingClientRect();
            r[k] = {box: [Math.round(bb.x), Math.round(bb.y + scrollY), Math.round(bb.width), Math.round(bb.height)]};
            for (const p of props) r[k][p] = cs.getPropertyValue(p); } return r; }""", [SEL, PROPS])
    b.close()
json.dump(out, open("/workspace/xwift-readme-template/study/computed-home.json","w"), indent=1)
for k in SEL:
    l, d = out["light"][k], out["dark"][k]
    if not l: print(k, "missing"); continue
    diff = {p: d[p] for p in PROPS if d and d[p] != l[p]}
    print(k, l["box"], {p: l[p] for p in PROPS if l[p] not in ("none","0px","normal","rgba(0, 0, 0, 0)","start","1","auto")}, "| DARK:", diff)
