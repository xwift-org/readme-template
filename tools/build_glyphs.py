"""Build brand/glyphs.json: outlined glyphs, advances and kerning for the styles the artwork uses.

Inter (OFL 1.1, rsms.me/inter) stands in for SF Pro; JetBrains Mono (OFL 1.1) stands in for SF Mono.
render.py reads the JSON with the standard library only, so no font file ships and no font is embedded.
Needs fonttools and uharfbuzz:  python3 -m pip install fonttools uharfbuzz
"""
import io, json, pathlib, itertools
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTER = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
MONO = "/usr/share/fonts/truetype/sand-box/google/JetBrains Mono/JetBrainsMono-VariableFont_wght.ttf"
# name: (file, axes). opsz follows the size each style is used at on swift.org (14 = text, 32 = display).
STYLES = {
    "text-400": (INTER, {"wght": 400, "opsz": 14}), "text-500": (INTER, {"wght": 500, "opsz": 14}),
    "text-600": (INTER, {"wght": 600, "opsz": 22}), "text-700": (INTER, {"wght": 700, "opsz": 20}),
    "mid-400": (INTER, {"wght": 400, "opsz": 24}), "mid-500": (INTER, {"wght": 500, "opsz": 24}),
    "display-400": (INTER, {"wght": 400, "opsz": 32}), "display-500": (INTER, {"wght": 500, "opsz": 32}),
    "display-600": (INTER, {"wght": 600, "opsz": 32}),
    "mono-400": (MONO, {"wght": 400}), "mono-600": (MONO, {"wght": 600}),
}
CHARS = "".join(chr(c) for c in range(32, 127)) + "’‘“”–—·•…→←✓×é©®"

def build(path, axes):
    vf = TTFont(path)
    inst = instancer.instantiateVariableFont(vf, axes, inplace=False)
    buf = io.BytesIO(); inst.save(buf); data = buf.getvalue()
    upm = inst["head"].unitsPerEm
    cmap = inst.getBestCmap(); gs = inst.getGlyphSet(); hmtx = inst["hmtx"]
    hbf = hb.Font(hb.Face(data))
    glyphs = {}
    for ch in CHARS:
        gn = cmap.get(ord(ch))
        if not gn: continue
        pen = SVGPathPen(gs, lambda v: f"{v:.0f}")
        gs[gn].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))  # y down
        glyphs[ch] = [hmtx[gn][0], pen.getCommands()]
    def adv(text):
        b = hb.Buffer(); b.add_str(text); b.guess_segment_properties()
        hb.shape(hbf, b, {"kern": True, "liga": False, "calt": False})
        return [p.x_advance for p in b.glyph_positions]
    kern = {}
    keys = [c for c in glyphs if c != " "]
    for a, b in itertools.product(keys, keys):
        k = adv(a + b)[0] - glyphs[a][0]
        if k: kern[a + b] = k
    os2 = inst["OS/2"]
    return {"upm": upm, "ascender": os2.sTypoAscender, "descender": os2.sTypoDescender,
            "capHeight": getattr(os2, "sCapHeight", 0), "xHeight": getattr(os2, "sxHeight", 0),
            "glyphs": glyphs, "kern": kern}

out = {"_note": __doc__.strip().splitlines()[0] + " Inter and JetBrains Mono are under the SIL Open Font License 1.1.",
       "styles": {}}
for name, (path, axes) in STYLES.items():
    out["styles"][name] = build(path, axes)
    print(name, len(out["styles"][name]["glyphs"]), "glyphs", len(out["styles"][name]["kern"]), "kern pairs")
p = ROOT / "brand" / "glyphs.json"
p.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
print(p, p.stat().st_size // 1024, "KB")
