"""Compositions: every block of the swift.org layout, redrawn for a README column.

All blocks are W (980) units wide: swift.org's content column. Values in comments are swift.org's
computed styles at 1280 px (see swiftorg-spec.md).
"""
import math
from render_base import (W, THEMES, FOOTER, BUTTON, GH_BG, Text, baseline, svg_doc, stops, fill_attr, rgba, esc, bird)
from art import ribbon, wave, grain, rrect, icon

# ---------------------------------------------------------------- shared pieces
PALETTES = {  # ribbon colours, picked to sit in swift.org's warm/violet family without reusing its files
    "pink":   [(0, "#ffd0ec"), (0.45, "#f99ad4"), (1, "#f070c0")],
    "gold":   [(0, "#ffd23a"), (0.5, "#ffb000"), (1, "#ff7a00")],
    "flame":  [(0, "#ffc94a"), (0.6, "#ff8a1f"), (1, "#f2542d")],
    "white":  [(0, "#ffffff"), (1, "#fff1e6")],
    "violet": [(0, "#b49cff"), (0.5, "#8a63f0"), (1, "#6a43d9")],
    "lilac":  [(0, "#f3c6ff"), (1, "#b48cf2")],
    "sky":    [(0, "#bfe8ff"), (1, "#6fb8ff")],
}

def nav(t, theme, mode, items, cta, y=0, h=67):
    """swift.org .site-navigation: 67 px bar, translucent, 19 px items with 12/15 px pill padding."""
    th = THEMES[theme]; out = []
    col, a = th["nav_bg"]
    out.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="{col}" fill-opacity="{a}"/>')
    if th["nav_shadow"]:
        out.append(f'<rect x="0" y="{y + h}" width="{W}" height="1" fill="#000" fill-opacity="{th["nav_shadow"] * 1.6:.2f}"/>')
    b, bw = bird(20, y + 16, 34, mode)
    out.append(b)
    out.append(t.run("Xwift", "text-500", 27, 20 + bw + 6, y + 43, th["nav_text"], track=-0.01))
    # items right-aligned to x = 960, each a 5 px link pad + 15 px span pad
    x = W - 20
    labels = list(items) + ["|", cta]
    widths = []
    for lab in labels:
        widths.append(2 + 30 if lab == "|" else t.width(lab, "text-400", 19) + 40)
    x -= sum(widths)
    for lab, wd in zip(labels, widths):
        if lab == "|":
            out.append(f'<rect x="{x + 15:.1f}" y="{y + 24.5}" width="2" height="18" fill="{th["nav_text"]}"/>')
        else:
            out.append(t.run(lab, "text-400", 19, x + 20, y + 40, th["nav_text"]))
        x += wd
    return "".join(out)

def swoop_band(uid, theme, y, h, seed=0, kind="hero", reveal=None):
    """The wide multi-strand swoop that closes each swift.org section (swoop-0/1/2)."""
    rows = {  # (palette, y fraction, width, wave count, phase)
        "hero":  [("gold", 0.20, 84, 1.2, 0.2), ("white", 0.34, 34, 1.3, 2.4), ("violet", 0.47, 120, 1.0, 0.9),
                  ("pink", 0.62, 76, 1.1, 1.8), ("white", 0.72, 30, 1.0, 1.1), ("gold", 0.84, 80, 0.9, 3.0)],
        "cool":  [("sky", 0.24, 60, 1.0, 0.5), ("violet", 0.42, 110, 0.9, 1.4), ("white", 0.36, 26, 1.2, 2.2),
                  ("flame", 0.60, 80, 1.1, 2.9), ("pink", 0.74, 54, 1.0, 0.8), ("gold", 0.86, 50, 0.8, 1.9)],
        "warm":  [("lilac", 0.24, 70, 1.0, 1.0), ("gold", 0.42, 110, 0.9, 1.7), ("white", 0.36, 28, 1.1, 2.6),
                  ("flame", 0.58, 84, 1.0, 0.3), ("violet", 0.72, 60, 1.2, 2.0), ("pink", 0.84, 44, 0.9, 2.8)],
    }[kind]
    defs, body = [], []
    for i, (pal, fy, wd, k, ph) in enumerate(rows):
        pts = [(x, yy - (x / W - 0.5) * h * 0.45) for x, yy in wave(-80, W + 80, y + h * fy, h * 0.13, 0.55 * k, ph + seed, 9)]
        d, b = ribbon(f"{uid}{i}", pts, wd, PALETTES[pal], twists=0.8 + 0.3 * i % 1.2, phase=0.2 * i,
                      strands=22, seed=seed * 10 + i + 3, ends=(0.0, 0.0), n=120,
                      body_opacity=0.9, pinch=0.5, hi=0.2 if pal != "white" else 0.0, haze=0.45, scatter=0.22,
                      reveal=(reveal[0] + 0.12 * i, reveal[1]) if reveal else None)
        defs.append(d); body.append(b)
    return "".join(defs), "".join(body)

def fade(uid, y0, y1, color, up=False):
    a, b = (0, 1) if not up else (1, 0)
    return (f'<linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity="{a}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="{b}"/></linearGradient>',
            f'<rect x="0" y="{y0}" width="{W}" height="{y1 - y0}" fill="url(#{uid})"/>')

def button(t, label, cx, y, size=35, padx=81, pady=15, radius=43):
    """swift.org install button: 35 px / 42 px line, 15/81 px padding, 43 px radius, #ff7f00 -> #f05238."""
    tw = t.width(label, "display-400", size, track=0)
    w = tw + 2 * padx; h = size * 1.2 + 2 * pady; x = cx - w / 2
    d = (f'<linearGradient id="btn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BUTTON[0]}"/>'
         f'<stop offset="1" stop-color="{BUTTON[1]}"/></linearGradient>')
    b = rrect(x, y, w, h, radius, 'fill="url(#btn)"') + t.run(label, "display-400", size, cx, baseline(y + pady, size * 1.2, size), "#ffffff", "middle", track=0)
    return d, b, h

# ---------------------------------------------------------------- hero (#what-is-swift)
HERO_RIBBONS = [  # (palette, points, width, twists, phase, seed)
    ("lilac", [(-70, 700), (0, 600), (60, 480), (95, 380)], 44, 0.5, 0.3, 15),
    ("pink",  [(-40, 660), (40, 520), (70, 380), (45, 250), (80, 130), (170, 62), (285, 72), (365, 140), (370, 225), (310, 272)], 92, 1.3, 0.12, 11),
    ("white", [(-40, 700), (75, 570), (140, 430), (175, 295), (230, 175), (325, 105), (440, 82)], 34, 1.1, 0.35, 12),
    ("gold",  [(-70, 580), (60, 480), (150, 360), (220, 235), (295, 140), (395, 85), (500, 92), (575, 145), (615, 210)], 84, 1.2, 0.05, 13),
]

PAD = 20  # swift.org .site-navigation .wrapper side padding

def hero(theme, mode, cfg):
    """cfg: title (list of lines), sub, button, caption, create, cards [(icon, title, text)], chips [label],
    nav_items, nav_cta. Geometry is swift.org's hero at 1280 px, shifted into the 980 px column."""
    th = THEMES[theme]; t = Text(); defs = []; body = []
    H = 1135
    # background: swift.org --homepage-hero-bg (179deg)
    defs.append(f'<linearGradient id="hbg" x1="0.49" y1="0" x2="0.51" y2="1">{stops(th["hero_bg"])}</linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#hbg)"/>')
    gd, gb = grain("hgrain", W, H, 0.05 if theme == "light" else 0.07)
    defs.append(gd); body.append(gb)
    # ribbons (drawn in once, like swift.org's hero canvas animation)
    for i, (pal, pts, wd, tw, ph, sd) in enumerate(HERO_RIBBONS):
        d, b = ribbon(f"hr{i}", pts, wd, PALETTES[pal], twists=tw, phase=ph, seed=sd, strands=30,
                      shade={"pink": "#d1489e", "white": "#e8a0c8", "lilac": "#9a63c9"}.get(pal, "#e0560a"), reveal=(0.15 * i, 1.7),
                      body_opacity=0.95, pinch=0.4, hi=0.38 if pal != "white" else 0.0, haze=0.35, scatter=0.2)
        defs.append(d); body.append(b)
    # navigation bar over the art
    body.append(nav(t, theme, mode, cfg["nav_items"], cfg["nav_cta"]))
    # title-0: 56/67.2, 600, centred, top 302, margin-bottom 30
    for i, line in enumerate(cfg["title"]):
        body.append(t.run(line, "display-600", 56, W / 2, baseline(302 + 67.2 * i, 67.2, 56), th["hero_text"], "middle"))
    ty = 302 + 67.2 * len(cfg["title"])
    # sub-text h2: 32/51.2, 400, margin 20 0 60
    sy = ty + 30 + 20 - 0  # swift.org: h1 margin 30 + h2 margin-top 20 ... collapsed -> 467 for two lines
    sy = 467 + (ty - 436.4)
    body.append(t.run(cfg["sub"], "display-400", 32, W / 2, baseline(sy, 51.2, 32), th["hero_text"], "middle"))
    by = sy + 51.2 + 60
    bd, bb, bh = button(t, cfg["button"], W / 2, by)
    defs.append(bd); body.append(bb)
    cy = by + bh + 11
    body.append(t.run(cfg["caption"], "text-500", 17, W / 2, baseline(cy, 27.2, 17), th["caption"], "middle", opacity=0.66))
    hy = cy + 27.2 + 70
    body.append(t.run(cfg["create"], "display-400", 32, W / 2, baseline(hy, 51.2, 32), th["text"], "middle"))
    # bottom swoop (swoop-0) sits behind the cards' lower half
    sd_, sb_ = swoop_band("hs", theme, 880, 300, seed=0.3, kind="hero", reveal=(0.6, 1.8))
    defs.append(sd_); body.append(sb_)
    # primary cards: 313x128, gap 20, radius 36, padding 25, rgba(255,177,100,.9) / #23344a
    py = hy + 51.2 + 29
    n = len(cfg["cards"]); cw = (W - 2 * PAD - 20 * (n - 1)) / n
    for i, (ic, title, text) in enumerate(cfg["cards"]):
        x = PAD + i * (cw + 20)
        body.append(rrect(x, py, cw, 128, 36, fill_attr(th["card_bg"])))
        body.append(icon(ic, x + 25, py + 25 + 7, 26, th["card_text"], 1.7))
        body.append(t.run(title, "text-600", 24, x + 62, baseline(py + 25, 38.4, 24), th["card_text"]))
        tb, _ = t.block(text, "text-400", 14, 19.6, x + 62, py + 25 + 38.4 + 1, cw - 62 - 25, th["card_text"])
        body.append(tb)
    # secondary chips: 46 px, gap 15, radius 36, 14 px
    qy = py + 128 + 20
    m = len(cfg["chips"]); qw = (W - 2 * PAD - 15 * (m - 1)) / m
    for i, lab in enumerate(cfg["chips"]):
        x = PAD + i * (qw + 15)
        body.append(rrect(x, qy, qw, 46, 36, fill_attr(th["card_bg"])))
        body.append(t.run(lab, "text-400", 14, x + qw / 2, baseline(qy + 12, 22.4, 14), th["card_text"], "middle"))
    # fade the last rows into GitHub's page colour so the next block continues the page
    fd, fb = fade("hfade", H - 60, H, GH_BG[theme])
    defs.append(fd); body.append(fb)
    label = " ".join(cfg["title"]) + " " + cfg["sub"]
    return svg_doc(W, H, label, "".join(body), t, "".join(defs))

# ---------------------------------------------------------------- pillar intro (.pillar-intro)
def intro(theme, text):
    """24 px / 1.45, centred, 720 px measure (swift.org .pillar-wrapper)."""
    th = THEMES[theme]; t = Text()
    top = 64
    tb, h = t.block(text, "mid-400", 24, 34.8, W / 2, top, 720, th["text"], "middle")
    H = top + h + 40
    return svg_doc(W, H, text, tb, t)

# ---------------------------------------------------------------- callout header (.callout .text)
def callout_head(theme, title, subtitle, align="start", top=60):
    """title-1 48/57.6 500 (margin -4 0 3), subtitle 24/28.8 500 (margin-bottom 22), callout padding 17."""
    th = THEMES[theme]; t = Text()
    x = 17 if align == "start" else W / 2
    y = top - 4
    b = t.run(title, "display-500", 48, x, baseline(y, 57.6, 48), th["text"], align)
    y += 57.6 + 3
    b += t.run(subtitle, "mid-500", 24, x, baseline(y, 28.8, 24), th["text"], align)
    H = y + 28.8 + 6
    return svg_doc(W, H, f"{title}. {subtitle}", b, t)

# ---------------------------------------------------------------- code card (pre.highlight)
import re as _re
SWIFT_KW = set("import func let var struct enum case class protocol extension public private internal static return if else guard for in while "
               "switch default mutating init self Self some any async await throws try where true false nil".split())
def tokens(line, lang):
    """Tiny highlighter with swift.org's syntax roles."""
    if lang == "shell":
        if line.startswith("$ "):
            return [("prompt", "$ "), ("plain", line[2:])]
        return [("comment" if line.startswith("#") else "output", line)]
    if lang == "json":
        out = []
        for m in _re.finditer(r'("(?:[^"\\]|\\.)*")(\s*:)?|([{}\[\],:])|(\s+)|([^\s"{}\[\],:]+)', line):
            if m.group(1): out.append(("type" if m.group(2) else "string", m.group(1)));  m.group(2) and out.append(("punct", m.group(2)))
            elif m.group(3): out.append(("punct", m.group(3)))
            else: out.append(("plain", m.group(0)))
        return out
    out = []
    pat = r'(//.*$)|("(?:[^"\\]|\\.)*")|(#\w+)|(@\w+)|(\b\d[\d_.]*\b)|(\b[A-Za-z_]\w*\b)(\s*\()?|(\.[a-z_]\w*)|([^\w\s])|(\s+)'
    for m in _re.finditer(pat, line):
        if m.group(1): out.append(("comment", m.group(1)))
        elif m.group(2): out.append(("string", m.group(2)))
        elif m.group(3): out.append(("keyword", m.group(3)))
        elif m.group(4): out.append(("keyword", m.group(4)))
        elif m.group(5): out.append(("number", m.group(5)))
        elif m.group(6):
            w = m.group(6)
            role = "keyword" if w in SWIFT_KW else "type" if w[0].isupper() else "call" if m.group(7) else "plain"
            out.append((role, w))
            if m.group(7): out.append(("punct", m.group(7)))
        elif m.group(8): out.append(("call", m.group(8)))
        else: out.append(("punct" if m.group(9) else "plain", m.group(0)))
    return out

def code_card(theme, code, lang="swift", label="Code example"):
    """pre: padding 28, 1 px border #d5d5d5 / #575757, radius 20, 14/21 code, bg rgba(255,255,255,.5) / #111727."""
    th = THEMES[theme]; syn = th["syntax"]; t = Text()
    lines = code.strip("\n").split("\n")
    x0, top = 17, 0
    w = W - 34; h = 56 + 21 * len(lines) + 2
    b = [rrect(x0 + 0.5, top + 0.5, w - 1, h - 1, 20, fill_attr(th["code_bg"]) + f' stroke="{th["code_border"]}"')]
    cw = t.width("M", "mono-400", 14)
    for i, line in enumerate(lines):
        x = x0 + 29; y = baseline(top + 29 + 21 * i, 21, 14)
        for role, txt in tokens(line, lang):
            col = syn.get(role, th["code_text"]) if role not in ("plain", "output") else th["code_text"]
            if txt.strip():
                b.append(t.run(txt, "mono-400", 14, x, y, col))
            x += cw * len(txt)
    H = h + 26
    return svg_doc(W, H, label + ":\n" + code.strip(), "".join(b), t)

# ---------------------------------------------------------------- section swoop (swoop-1 / swoop-2)
def swoop(theme, kind="cool", seed=1.0, tint=None):
    """A free-standing swoop band between sections. Edges fade to GitHub's page colour.
    tint: the next pillar's colour, shown softly behind the band."""
    H = 300; defs = []; body = []
    if tint:
        st = THEMES[theme][tint]
        mid = st[min(1, len(st) - 1)][1]
        defs.append(f'<radialGradient id="tint" cx="0.5" cy="0.55" r="0.75"><stop offset="0" stop-color="{mid}" stop-opacity="0.55"/>'
                    f'<stop offset="1" stop-color="{mid}" stop-opacity="0"/></radialGradient>')
        body.append(f'<rect width="{W}" height="{H}" fill="url(#tint)"/>')
    d, b = swoop_band(f"sw{kind}", theme, 10, H - 20, seed=seed, kind=kind, reveal=(0.2, 1.8))
    defs.append(d); body.append(b)
    f1d, f1b = fade("sf1", 0, 40, GH_BG[theme], up=True); f2d, f2b = fade("sf2", H - 40, H, GH_BG[theme])
    defs += [f1d, f2d]; body += [f1b, f2b]
    return svg_doc(W, H, "", "".join(body), None, "".join(defs))

# ---------------------------------------------------------------- closing: pillar-3 band + global footer
def closing(theme, mode, band, footer):
    """band: title, subtitle, links [label]. footer: columns [(heading or None, [items])], note.
    #pillar-3: gradient #e4937f -> #a268c1 36% -> #4b3773, padding 64/40, white 48/24 type, 17 px underlined links.
    footer.global-footer: #1e162e, padding 96 48 48, headings #fca76c 19.89/700, links 14 px #ebecf0."""
    th = THEMES[theme]; t = Text(); defs = []; body = []
    sw = 230  # swoop-2 overlap above the band
    by = sw
    bh = 64 + 57.6 - 4 + 3 + 28.8 + 22 + 30 + len(band["links"]) * (27.2 + 14) + 40 + 40
    st = th["pillar3"]
    defs.append(f'<linearGradient id="p3" x1="0" y1="0" x2="0" y2="1">{stops(st)}</linearGradient>')
    # warm lead-in from the page colour into the band's first stop, like pillar-2 handing over to pillar-3
    defs.append(f'<linearGradient id="lead" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GH_BG[theme]}"/>'
                f'<stop offset="0.45" stop-color="{th["pillar2"][-1][1] if theme == "light" else th["pillar2"][-1][1]}" stop-opacity="0.9"/>'
                f'<stop offset="1" stop-color="{st[0][1]}"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{by + 2}" fill="url(#lead)"/>')
    body.append(f'<rect y="{by}" width="{W}" height="{bh}" fill="url(#p3)"/>')
    d, b = swoop_band("cl", theme, by - 190, 330, seed=2.2, kind="warm", reveal=(0.2, 1.8))
    defs.append(d); body.append(b)
    y = by + 64 - 4
    body.append(t.run(band["title"], "display-500", 48, W / 2, baseline(y, 57.6, 48), "#ffffff", "middle")); y += 57.6 + 3
    body.append(t.run(band["subtitle"], "mid-500", 24, W / 2, baseline(y, 28.8, 24), "#ffffff", "middle")); y += 28.8 + 22 + 30 - 14
    for lab in band["links"]:
        y += 14
        bl = baseline(y, 27.2, 17)
        body.append(t.run(lab, "text-400", 17, W / 2, bl, "#ffffff", "middle"))
        lw = t.width(lab, "text-400", 17)
        body.append(f'<rect x="{W / 2 - lw / 2:.1f}" y="{bl + 2.5:.1f}" width="{lw:.1f}" height="1" fill="#ffffff" fill-opacity="0.5"/>')
        y += 27.2
    gd, gb = grain("clg", W, by + bh, 0.05)
    defs.append(gd); body.append(gb)
    # footer
    fy = by + bh
    cols = footer["columns"]
    rows = max(len(c[1]) for c in cols)
    fh = 96 + 36 + 15 + rows * 33 + 64 + 60 + 48
    body.append(f'<rect y="{fy}" width="{W}" height="{fh}" fill="{FOOTER["bg"]}"/>')
    cx0 = 59.5; colw = (W - cx0 - 48) / len(cols)
    for i, (head, items) in enumerate(cols):
        x = cx0 + i * colw; y = fy + 96
        if head is None:
            bb, bw = bird(x, y + 1, 34, "dark")
            body.append(bb + t.run("Xwift", "text-500", 29, x + bw + 6, y + 28, FOOTER["text"], track=-0.01))
        else:
            body.append(t.run(head, "text-700", 19.89, x, baseline(y + 6, 23.868, 19.89), FOOTER["heading"]))
        y += 36 + 15
        for it in items:
            body.append(t.run(it, "text-400", 14, x, baseline(y + 4.9, 22.4, 14), FOOTER["text"]))
            y += 33
    ny = fy + 96 + 36 + 15 + rows * 33 + 64
    for j, line in enumerate(footer["note"]):
        body.append(t.run(line, "text-400", 11, cx0, baseline(ny + j * 17, 17, 11), FOOTER["text"], opacity=0.85))
    H = fy + fh
    return svg_doc(W, H, band["title"] + ". " + band["subtitle"], "".join(body), t, "".join(defs))

# ---------------------------------------------------------------- repository banner (install/get-started hero)
def repo_banner(theme, mode, cfg):
    """A shorter hero for repository READMEs: nav, the repo name at title-0 size, the tagline at sub-text size,
    the kind as the orange button, swoop-0 underneath. Seeded by the repo name so each repo's ribbons differ."""
    th = THEMES[theme]; t = Text(); defs = []; body = []
    H = 640
    seed = sum(map(ord, cfg["name"])) % 97 / 97
    defs.append(f'<linearGradient id="rbg" x1="0.49" y1="0" x2="0.51" y2="1">{stops(th["hero_bg"])}</linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#rbg)"/>')
    gd, gb = grain("rgr", W, H, 0.05 if theme == "light" else 0.07); defs.append(gd); body.append(gb)
    dx = (seed - 0.5) * 60
    for i, (pal, pts, wd, tw, ph, sd) in enumerate(HERO_RIBBONS):
        pts2 = [(x * 0.82 + dx, y * 0.62 - 20) for x, y in pts]
        d, b = ribbon(f"rr{i}", pts2, wd * 0.8, PALETTES[pal], twists=tw, phase=ph + seed, seed=sd + int(seed * 50), strands=26,
                      shade={"pink": "#d1489e", "white": "#e8a0c8", "lilac": "#9a63c9"}.get(pal, "#e0560a"),
                      reveal=(0.15 * i, 1.6), body_opacity=0.95, pinch=0.4, hi=0.38 if pal != "white" else 0.0, haze=0.35, scatter=0.2)
        defs.append(d); body.append(b)
    labels = [l["label"] for l in cfg.get("links", [])][:4] or ["Install", "Usage", "Status"]
    body.append(nav(t, theme, mode, labels[:-1] if len(labels) > 1 else labels, labels[-1] if len(labels) > 1 else "README"))
    y = 200
    body.append(t.run(cfg["name"], "display-600", 56, W / 2, baseline(y, 67.2, 56), th["hero_text"], "middle")); y += 67.2 + 30
    tb, th_ = t.block(cfg["tagline"], "display-400", 32, 51.2, W / 2, y - 10, 860, th["hero_text"], "middle"); body.append(tb); y += th_ - 10 + 40
    bd, bb, bh = button(t, cfg.get("kind", "repository").capitalize(), W / 2, y, size=28, padx=41)
    defs.append(bd); body.append(bb)
    sd_, sb_ = swoop_band("rs", theme, H - 230, 240, seed=seed * 3, kind="hero", reveal=(0.5, 1.8))
    defs.append(sd_); body.append(sb_)
    fd, fb = fade("rfade", H - 60, H, GH_BG[theme]); defs.append(fd); body.append(fb)
    return svg_doc(W, H, f'{cfg["name"]}. {cfg["tagline"]}', "".join(body), t, "".join(defs))

# ---------------------------------------------------------------- platform cards (get-started boxes)
def platform_cards(theme, platforms):
    """Get Started boxes: 3 columns, gap 20, radius 20, padding 16/16/20, 24 px 600 title, 14 px text."""
    th = THEMES[theme]; t = Text(); body = []
    from render_base import STATUS_LABEL
    cols = 3; gap = 20; cw = (W - 2 * PAD - gap * (cols - 1)) / cols; ch = 112
    rows = (len(platforms) + cols - 1) // cols
    for i, p in enumerate(platforms):
        r, c = divmod(i, cols); x = PAD + c * (cw + gap); y = 24 + r * (ch + gap)
        body.append(rrect(x, y, cw, ch, 20, fill_attr(th["card_bg"])))
        body.append(t.run(p["name"], "text-600", 24, x + 20, baseline(y + 16, 28.8, 24), th["card_text"]))
        lab = STATUS_LABEL.get(p.get("status", ""), p.get("status", ""))
        lw = t.width(lab, "text-500", 12) + 20
        dot = {"working": "#2da44e", "in-progress": "#ffb000", "planned": "#8d8d8d"}.get(p.get("status"), "#8d8d8d")
        body.append(rrect(x + cw - 20 - lw - 12, y + 19, lw + 12, 24, 12, f'fill="{th["card_text"]}" fill-opacity="0.12"'))
        body.append(f'<circle cx="{x + cw - 20 - lw - 2:.1f}" cy="{y + 31}" r="3.5" fill="{dot}"/>')
        body.append(t.run(lab, "text-500", 12, x + cw - 20 - lw + 6, y + 35.5, th["card_text"]))
        tb, _ = t.block(p.get("note", ""), "text-400", 14, 19.6, x + 20, y + 16 + 28.8 + 10, cw - 40, th["card_text"])
        body.append(tb)
    H = 24 + rows * (ch + gap) - gap + 30
    label = "Platforms: " + "; ".join(f'{p["name"]}: {STATUS_LABEL.get(p.get("status",""), p.get("status",""))}. {p.get("note","")}' for p in platforms)
    return svg_doc(W, H, label, "".join(body), t)
