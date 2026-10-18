"""Local GitHub-like preview: GitHub Markdown API + github-markdown-css, screenshot light and dark.
usage: preview_local.py README.md out-prefix [--w 880]"""
import sys, json, time, pathlib, urllib.request, os
from playwright.sync_api import sync_playwright
md = pathlib.Path(sys.argv[1]).resolve(); pre = sys.argv[2]; w = 880
req = urllib.request.Request("https://api.github.com/markdown", data=json.dumps({"text": md.read_text(), "mode": "markdown"}).encode(),
                             headers={"Accept": "application/vnd.github+json", "Authorization": "token " + os.environ["GITHUB_TOKEN_BAIEHCLACA"]})
html = urllib.request.urlopen(req).read().decode()
css = (pathlib.Path(__file__).parent / "github-markdown.css").read_text()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    for scheme, bg in (("light", "#ffffff"), ("dark", "#0d1117")):
        page = f'<html><head><base href="file://{md.parent}/"><style>{css} body{{margin:0;background:{bg}}} .markdown-body{{box-sizing:border-box;width:{w + 64}px;padding:32px;margin:0 auto}}</style></head><body><article class="markdown-body">{html}</article></body></html>'
        f = pathlib.Path(f"/tmp/_prev_{scheme}.html"); f.write_text(page)
        pg = b.new_context(viewport={"width": w + 64, "height": 900}, color_scheme=scheme).new_page()
        pg.goto(f"file://{f}"); time.sleep(4)
        pg.screenshot(path=f"{pre}-{scheme}.png", full_page=True); print(f"{pre}-{scheme}.png")
    b.close()
