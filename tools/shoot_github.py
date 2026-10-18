"""Screenshot a README as github.com renders it (logged out, 1280 px, light and dark).
usage: shoot_github.py URL out-prefix   -> out-prefix-{light,dark}.png (README box only) and -page-*.png"""
import sys, time
from playwright.sync_api import sync_playwright
url, pre = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for scheme in ("light", "dark"):
        ctx = b.new_context(viewport={"width": 1280, "height": 1000}, color_scheme=scheme, device_scale_factor=1)
        pg = ctx.new_page(); pg.goto(url, wait_until="networkidle", timeout=90000)
        h = pg.evaluate("document.body.scrollHeight")
        for y in range(0, h + 1000, 500):
            pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.25)
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_function("Array.from(document.images).every(i => i.complete)", timeout=60000)
        time.sleep(4)
        el = pg.query_selector("article.markdown-body") or pg.query_selector(".markdown-body")
        box = el.bounding_box(); print(scheme, "readme box", box)
        el.screenshot(path=f"{pre}-{scheme}.png")
        pg.screenshot(path=f"{pre}-page-{scheme}.png", full_page=True)
        ctx.close()
    b.close()
