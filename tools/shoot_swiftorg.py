"""Screenshot swift.org pages at 1280px, light and dark, for reference only (refs/ is not published)."""
import sys, time
from playwright.sync_api import sync_playwright
OUT = "/workspace/xwift-readme-template/refs"
PAGES = {"home": "https://www.swift.org/", "install": "https://www.swift.org/install/",
         "get-started": "https://www.swift.org/get-started/", "community": "https://www.swift.org/community/",
         "packages": "https://www.swift.org/packages/", "blog": "https://www.swift.org/blog/",
         "documentation": "https://www.swift.org/documentation/"}
sel = sys.argv[1:] or list(PAGES)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for scheme in ("light", "dark"):
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, color_scheme=scheme, device_scale_factor=1)
        pg = ctx.new_page()
        for name in sel:
            pg.goto(PAGES[name], wait_until="networkidle", timeout=60000)
            h = pg.evaluate("document.body.scrollHeight")
            for y in range(0, h, 400):
                pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.12)
            pg.evaluate("window.scrollTo(0,0)"); time.sleep(3)
            pg.screenshot(path=f"{OUT}/swiftorg-{name}-{scheme}-fold.png")
            pg.screenshot(path=f"{OUT}/swiftorg-{name}-{scheme}-full.png", full_page=True)
            print(name, scheme, h, pg.url)
        ctx.close()
    b.close()
