"""Shared constants and helpers for the Xwift README renderer.

Every measurement here comes from swift.org's computed styles at a 1280 px viewport
(see swiftorg-spec.md). One SVG unit is one CSS pixel of swift.org's 980 px content column,
so an SVG drawn at width="100%" in a README maps the README column onto that column.
"""
import html, json, math, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
PAL = json.loads((BRAND / "palette.json").read_text())
BIRD = json.loads((BRAND / "bird.json").read_text())
GLYPHS = json.loads((BRAND / "glyphs.json").read_text())["styles"]

W = 980  # swift.org .content-wrapper / .callout max-width

# GitHub's page colours: blocks fade into these at their edges so stacked images read as one page.
GH_BG = {"light": "#ffffff", "dark": "#0d1117"}

THEMES = {
    "light": dict(
        page=GH_BG["light"], text="#051416", hero_text="#3d3d3d", nav_text="#3d3d3d",
        nav_bg=("#ffffff", 0.5), nav_shadow=0.05, caption="#3d3d3d",
        hero_bg=[(0.03, "#fac685"), (0.87, "#fbdab0"), (1.0, "#ffffff")],
        card_bg=("#ffb164", 0.9), card_text="#801a1a",
        pillar1=[(0.0, "#ffffff"), (0.75, "#d9f2ff"), (0.9, "#fff3d8")],
        pillar2=[(0.0, "#fff3d8"), (0.28, "#fdd9a1"), (1.0, "#e4937f")],
        pillar3=[(0.0, "#e4937f"), (0.36, "#a268c1"), (1.0, "#4b3773")],
        code_bg=("#ffffff", 0.5), code_border="#d5d5d5", code_text="#051416",
        link="#384fea", rule="#e2e2e2", muted="#8d8d8d", chip_bg="#e2e2e2", chip_text="#4d4d4d",
        surface="#fafafa", card_primary=("#ffffff", 0.9), card_secondary="#ececec",
        syntax=dict(comment="#707f8c", keyword="#ad3da4", string="#d12f1b", number="#272ad8",
                    type="#703daa", call="#2d6469", ident="#b181ec", plain="#000000", punct="#2d6469",
                    attr="#947100", prompt="#707f8c"),
    ),
    "dark": dict(
        page=GH_BG["dark"], text="#ffffff", hero_text="#ffffff", nav_text="#ffffff",
        nav_bg=("#000000", 0.3), nav_shadow=0.0, caption="#dedede",
        hero_bg=[(0.0, "#144173"), (0.68, "#141228"), (0.92, "#144173"), (1.0, GH_BG["dark"])],
        card_bg=("#23344a", 1.0), card_text="#ffffff",
        pillar1=[(0.0, "#144173"), (0.57, "#000000"), (0.88, "#350839"), (0.99, "#df6b40")],
        pillar2=[(0.0, "#df6b40"), (1.0, "#ffac64")],
        pillar3=[(0.0, "#ffac64"), (0.28, "#a268c1"), (1.0, "#4b3773")],
        code_bg=("#111727", 1.0), code_border="#575757", code_text="#ffffff",
        link="#1ec1fd", rule="#384461", muted="#c4c4c4", chip_bg="#172538", chip_text="#c4c4c4",
        surface="rgb(5,20,35)", card_primary=("#23344a", 0.9), card_secondary="#384461",
        syntax=dict(comment="#7f8c98", keyword="#ff79b3", string="#ff8170", number="#d9c97c",
                    type="#dabaff", call="#78c2b3", ident="#b181ec", plain="#ffffff", punct="#ffffff",
                    attr="#cc9768", prompt="#7f8c98"),
    ),
}
FOOTER = dict(bg="#1e162e", text="#ebecf0", heading="#fca76c")
BUTTON = ("#ff7f00", "#f05238")  # swift.org install button, to bottom right
PLATFORM_ORDER = ["macOS", "Windows", "Linux", "Android", "iOS", "Web"]
STATUS_LABEL = {"working": "Working", "in-progress": "In progress", "planned": "Planned"}

def esc(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- outlined text
# Inter's dynamic tracking (rsms.me/inter/dynmetrics) tracks SF Pro's optical tracking closely.
def tracking(size): return -0.0223 + 0.185 * math.exp(-0.1745 * size)

STYLE_FOR = {  # (weight, size) on swift.org -> glyph style
    "title-0": "display-600", "title-1": "display-500", "title-2": "mid-500", "sub": "display-400",
    "button": "display-400", "h2": "display-400", "nav": "text-400", "caption": "text-500",
    "card-title": "text-600", "small": "text-400", "body": "text-400", "intro": "mid-400",
    "footer-h": "text-700", "mono": "mono-400", "mono-b": "mono-600", "body-500": "text-500",
}

class Text:
    """Lays out text with the glyph atlas and emits <use> references to shared glyph defs."""
    def __init__(self):
        self.used = {}  # (style, char) -> id

    def _gid(self, style, ch):
        k = (style, ch)
        if k not in self.used:
            self.used[k] = f"g{len(self.used):x}"
        return self.used[k]

    def width(self, s, style, size, track=None):
        st = GLYPHS[style]; sc = size / st["upm"]
        tr = (tracking(size) if track is None else track) * size
        if style.startswith("mono"): tr = 0
        w = 0.0; prev = None
        for ch in s:
            g = st["glyphs"].get(ch) or st["glyphs"]["?"]
            if prev: w += st["kern"].get(prev + ch, 0) * sc
            w += g[0] * sc + tr; prev = ch
        return w - (tr if s else 0)

    def run(self, s, style, size, x, y, fill, anchor="start", track=None, opacity=None, extra=""):
        """y is the baseline."""
        st = GLYPHS[style]; sc = size / st["upm"]
        tr = (tracking(size) if track is None else track) * size
        if style.startswith("mono"): tr = 0
        w = self.width(s, style, size, track)
        if anchor == "middle": x -= w / 2
        elif anchor == "end": x -= w
        out = []; prev = None; cx = x
        for ch in s:
            g = st["glyphs"].get(ch) or st["glyphs"]["?"]
            if prev: cx += st["kern"].get(prev + ch, 0) * sc
            if g[1]:
                out.append(f'<use href="#{self._gid(style, ch)}" transform="matrix({sc:.5f} 0 0 {sc:.5f} {cx:.2f} {y:.2f})"/>')
            cx += g[0] * sc + tr; prev = ch
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return f'<g fill="{fill}"{op}{extra}>' + "".join(out) + "</g>"

    def wrap(self, s, style, size, max_w, track=None):
        lines, cur = [], ""
        for word in s.split():
            t = (cur + " " + word).strip()
            if self.width(t, style, size, track) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur); cur = word
        if cur: lines.append(cur)
        return lines

    def block(self, s, style, size, lh, x, top, max_w, fill, anchor="start", track=None, opacity=None):
        """Paragraph laid out like CSS: line boxes of height lh starting at top. Returns (svg, height)."""
        lines = []
        for para in s.split("\n"):
            lines += self.wrap(para, style, size, max_w, track) if para.strip() else [""]
        out = [self.run(l, style, size, x, baseline(top + i * lh, lh, size), fill, anchor, track, opacity)
               for i, l in enumerate(lines) if l]
        return "".join(out), len(lines) * lh

    def defs(self):
        out = []
        for (style, ch), gid in self.used.items():
            out.append(f'<path id="{gid}" d="{GLYPHS[style]["glyphs"][ch][1]}"/>')
        return "".join(out)

def baseline(top, lh, size, asc=0.96875, desc=0.2421875):
    """Baseline of a CSS line box (Inter's typo metrics, as browsers place SF and Inter)."""
    return top + (lh - (asc + desc) * size) / 2 + asc * size

# ---------------------------------------------------------------- svg helpers
def rgba(c):
    return (c[0], c[1]) if isinstance(c, tuple) else (c, 1.0)

def fill_attr(c, attr="fill"):
    col, a = rgba(c)
    return f'{attr}="{col}"' + (f' {attr}-opacity="{a}"' if a < 1 else "")

def stops(st, opacity=None):
    return "".join(f'<stop offset="{o:.3f}" stop-color="{c}"' + (f' stop-opacity="{opacity}"' if opacity is not None else "") + "/>"
                   for o, c in st)

def svg_doc(w, h, label, body, text=None, defs=""):
    d = (text.defs() if text else "") + defs
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h:.0f}" '
            f'viewBox="0 0 {w} {h:.0f}" role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>'
            f'<defs>{d}</defs>{body}</svg>\n')

def bird(x, y, h, mode="light", stroke_px=1.3):
    """The Xwift mark (brand/bird.json), traced line art. Returns (svg, width)."""
    col = BIRD["colors_dark"] if mode == "dark" else BIRD["colors"]
    vw, vh = BIRD["viewBox"][2], BIRD["viewBox"][3]
    s = h / vh; sw = stroke_px / s
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})">'
            f'<path d="{BIRD["violet"]}" fill="{col["violet"]}" fill-rule="evenodd" stroke="{col["violet"]}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<path d="{BIRD["orange"]}" fill="{col["orange"]}" fill-rule="evenodd" stroke="{col["orange"]}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'</g>'), vw * s
