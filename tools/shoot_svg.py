"""Render SVG files to PNG in headless Chrome after their animations finish. usage: shoot_svg.py out.png a.svg [b.svg ...] [--w 980] [--bg #fff]"""
import sys, time, pathlib
from playwright.sync_api import sync_playwright
args = sys.argv[1:]; w = 980; bg = "#ffffff"
if "--w" in args: i = args.index("--w"); w = int(args[i + 1]); del args[i:i + 2]
if "--bg" in args: i = args.index("--bg"); bg = args[i + 1]; del args[i:i + 2]
out, files = args[0], args[1:]
html = f'<body style="margin:0;background:{bg}">' + "".join(f'<img src="file://{pathlib.Path(f).resolve()}" style="display:block;width:{w}px">' for f in files)
pathlib.Path("/tmp/_shoot.html").write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": w, "height": 600})
    pg.goto("file:///tmp/_shoot.html"); time.sleep(3.5)
    pg.screenshot(path=out, full_page=True); b.close()
print(out)
