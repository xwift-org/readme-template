"""Side-by-side: swift.org at 1280 px (scaled so its 980 px column matches the README column) vs the README on github.com."""
import sys
from PIL import Image, ImageDraw, ImageFont
gh_prefix, out_prefix = sys.argv[1], sys.argv[2]
REF = "/workspace/xwift-readme-template/refs/swiftorg-home-{}-full.png"
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
for s in ("light", "dark"):
    import json, os
    gh = Image.open(f"{gh_prefix}-{s}.png").convert("RGB")
    meta = json.load(open(f"{gh_prefix}-{s}.json")) if os.path.exists(f"{gh_prefix}-{s}.json") else {"x": 32, "y": 32, "w": gh.width - 64}
    col = meta["w"]  # rendered width of the first README image = the README column
    gh = gh.crop((0, max(0, int(meta["y"]) - 0), gh.width, gh.height))  # start at the hero, like swift.org starts at its nav
    ref = Image.open(REF.format(s)).convert("RGB")
    k = col / 980; ref = ref.resize((round(ref.width * k), round(ref.height * k)), Image.LANCZOS)
    bg = (255, 255, 255) if s == "light" else (13, 17, 23); fg = (30, 30, 30) if s == "light" else (230, 230, 230)
    top = 50; gap = 40
    for name, h in (("full", None), ("fold", 1250)):
        H = top + (h or max(ref.height, gh.height))
        c = Image.new("RGB", (ref.width + gap + gh.width, H), bg)
        c.paste(ref.crop((0, 0, ref.width, min(ref.height, H - top))), (0, top))
        c.paste(gh.crop((0, 0, gh.width, min(gh.height, H - top))), (ref.width + gap, top))
        d = ImageDraw.Draw(c)
        d.text((10, 12), f"swift.org, 1280 px ({s}), scaled x{k:.3f} so its 980 px column = README column", fill=fg, font=font)
        d.text((ref.width + gap + 10, 12), f"Xwift README on github.com ({s})", fill=fg, font=font)
        c.save(f"{out_prefix}-{name}-{s}.png", optimize=True); print(f"{out_prefix}-{name}-{s}.png", c.size)
