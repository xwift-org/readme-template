"""Artwork compositions for the Xwift org profile and repo banners."""
import math
import art
from render_base import THEMES, PAL, BIRD, SANS, MONO, bird, svg_doc, fade_in, esc, PLATFORM_ORDER

def cols(mode):
    v = PAL["violet"] if mode == "light" else "#9C85FF"
    return PAL["ion"], v, PAL["pulse"], PAL["ember"]

def frame(W, H, t, defs, body, label, radius=20, cid="clip", bg=None):
    defs.append(f'<clipPath id="{cid}"><rect width="{W}" height="{H}" rx="{radius}"/></clipPath>')
    inner = (f'<defs>{"".join(defs)}</defs><g clip-path="url(#{cid})"><rect width="{W}" height="{H}" fill="{bg or t["bg"]}"/>'
             f'{"".join(body)}</g><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{radius}" fill="none" stroke="{t["rule"]}"/>')
    return svg_doc(W, H, label, inner)

def shade(mode): return 0.1 if mode == "light" else 0.28
def fop(mode): return 0.2 if mode == "light" else 0.32

def add_grain(defs, body, W, H, mode, uid="gr"):
    defs.append(art.grain(uid, 0.06 if mode == "light" else 0.1))
    body.append(f'<rect width="{W}" height="{H}" filter="url(#{uid})"/>')

def halo(defs, t, uid="halo"):
    defs.append(f'<radialGradient id="{uid}"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="0.95"/>'
                f'<stop offset="1" stop-color="{t["bg"]}" stop-opacity="0"/></radialGradient>')

# ------------------------------------------------------------------ org hero
def org_hero(mode):
    t = THEMES[mode]; W, H = 960, 640
    I, V, N, E = cols(mode)
    defs, body = [], []
    fo = fop(mode)
    d, b = art.fields("hf", W, H, [(120, 60, 230, V, fo), (860, 90, 220, I, fo), (760, 640, 260, E, fo),
                                   (180, 620, 220, N, fo * 0.9), (480, 330, 180, V, fo * 0.4)], blur=70)
    defs.append(d); body.append(b)
    for uid, pts, w, c, tw, ph in [("b1", [(-60, 140), (260, 40), (520, 300), (W + 60, 120)], (120, 160), [V, I], 0.8, 0.2),
                                   ("b2", [(-60, 470), (300, 330), (640, 560), (W + 60, 380)], (140, 110), [N, E], 0.7, 1.0)]:
        dd, bb = art.ribbon(uid, pts, w, c, twist=tw, phase=ph, opacity=0.22 if mode == "light" else 0.3, sheen=False, shade=0)
        defs.append(dd); body.append(bb)
    bh = 118; bw = BIRD["viewBox"][2] / BIRD["viewBox"][3] * bh; bx, by = W / 2 - bw / 2, 52
    ox, oy = W / 2 + 30, by + bh * 0.42
    R = [("r1", [(ox, oy), (ox + 150, oy - 90), (ox + 330, oy - 150), (W + 40, oy - 40)], (10, 96), [E, N, V], 1.2, 0.2, 0.2),
         ("r2", [(ox, oy + 8), (ox + 170, oy + 40), (ox + 320, oy - 30), (W + 30, oy + 150)], (6, 70), [N, E], 1.6, 0.6, 0.45),
         ("r3", [(ox, oy + 14), (ox + 120, oy + 120), (ox + 300, oy + 40), (W - 10, H * 0.62)], (4, 44), [V, I], 0.9, 0.1, 0.65),
         ("l1", [(ox - 60, oy), (ox - 230, oy - 120), (ox - 420, oy - 120), (-40, oy + 10)], (10, 92), [I, V, N], 1.3, 0.4, 0.3),
         ("l2", [(ox - 60, oy + 10), (ox - 250, oy + 30), (ox - 380, oy + 140), (-30, H * 0.66)], (6, 60), [V, I], 1.1, 0.9, 0.5),
         ("g1", [(-40, H - 20), (240, H - 230), (620, H + 40), (W + 40, H - 190)], (110, 70), [I, V, N, E], 1.4, 0.3, 0.8),
         ("g2", [(-40, H - 140), (300, H - 10), (700, H - 260), (W + 40, H - 40)], (80, 120), [N, E, V], 1.1, 1.2, 0.95),
         ("g3", [(-40, H - 70), (200, H - 120), (520, H - 150), (W + 40, H - 250)], (30, 60), [E, N], 2.2, 0.0, 1.1)]
    for uid, pts, w, c, tw, ph, dl in R:
        dd, bb = art.ribbon(uid, pts, w, c, twist=tw, phase=ph, opacity=0.92 if uid[0] != "g" else 0.85,
                            anim=art.enter(dl, dx=-(pts[3][0] - pts[0][0]) * 0.04), strands=2, shade=shade(mode))
        defs.append(dd); body.append(bb)
    body.append(art.flight(f"M{ox} {oy} C{ox+200} {oy-200} {ox+380} {oy-20} {W} {oy-110}", t["text"], 0.35))
    body.append(art.flight(f"M{ox-60} {oy} C{ox-260} {oy-220} {ox-460} {oy-10} 0 {oy-120}", t["text"], 0.35, dur=9))
    add_grain(defs, body, W, H, mode)
    halo(defs, t)
    body.append(f'<ellipse cx="{W/2}" cy="{by+bh/2}" rx="120" ry="95" fill="url(#halo)"/>')
    body.append(bird(bx, by, bh, mode=mode)[0])
    body.append(f'<ellipse cx="{W/2}" cy="352" rx="430" ry="100" fill="url(#halo)"/>')
    body.append(f'<g>{fade_in(0.5,0.6)}<text x="{W/2}" y="300" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" letter-spacing="2.4" fill="{t["accent"]}">XWIFT</text></g>')
    body.append(f'<g>{fade_in(0.7,0.6)}<text x="{W/2}" y="364" text-anchor="middle" font-family="{SANS}" font-size="58" font-weight="700" letter-spacing="-2" fill="{t["text"]}">Write once. Run everything.</text></g>')
    body.append(f'<g>{fade_in(0.9,0.6)}<text x="{W/2}" y="406" text-anchor="middle" font-family="{SANS}" font-size="20" letter-spacing="-0.2" fill="{t["muted"]}">A cross-platform toolchain, UI framework and system APIs.</text></g>')
    return frame(W, H, t, defs, body, "Xwift. Write once. Run everything. A cross-platform toolchain, UI framework and system APIs.")

# ------------------------------------------------------------- platform strip
def org_platforms(mode):
    t = THEMES[mode]; W, H = 960, 210
    I, V, N, E = cols(mode)
    defs, body = [], []
    d, b = art.fields("pf", W, H, [(80, 200, 160, I, fop(mode)), (480, 230, 180, V, fop(mode) * 0.8), (880, 200, 160, E, fop(mode))], blur=50)
    defs.append(d); body.append(b)
    yc = 150
    fr = art.wave_frames(-20, W + 20, yc, 16, 2.5, phase=0.6)
    dd, bb = art.ribbon("pw", None, 46, [I, V, N, E], twist=5.0, phase=0.4, frames_in=fr, strands=2, shade=shade(mode), env_pow=0.25,
                        anim=art.enter(0.1, dx=-30))
    defs.append(dd); body.append(bb)
    fr2 = art.wave_frames(-20, W + 20, yc + 12, 22, 1.5, phase=2.2)
    dd, bb = art.ribbon("pw2", None, 18, [E, N, V, I], twist=3.0, phase=1.0, frames_in=fr2, shade=0, sheen=False, opacity=0.55, env_pow=0.3)
    defs.append(dd); body.append(bb)
    n = len(PLATFORM_ORDER); cw = W / n
    nodecol = [I, V, N, E, V, I]
    for i, p in enumerate(PLATFORM_ORDER):
        cx = cw * i + cw / 2
        y = yc + 16 * math.sin(2 * math.pi * 2.5 * ((cx + 20) / (W + 40)) + 0.6)
        if i:
            body.append(f'<line x1="{cw*i:.1f}" y1="36" x2="{cw*i:.1f}" y2="96" stroke="{t["rule"]}"/>')
        body.append(f'<text x="{cx:.1f}" y="52" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["muted"]}">{i+1:02d}</text>')
        body.append(f'<text x="{cx:.1f}" y="84" text-anchor="middle" font-family="{SANS}" font-size="21" font-weight="600" letter-spacing="-0.4" fill="{t["text"]}">{p}</text>')
        body.append(f'<line x1="{cx:.1f}" y1="98" x2="{cx:.1f}" y2="{y-9:.1f}" stroke="{nodecol[i]}" stroke-opacity="0.6" stroke-dasharray="2 3"/>')
        body.append(f'<g>{fade_in(0.4 + 0.15*i, 0.3, 0.4 + 0.15*n + 0.3)}<circle cx="{cx:.1f}" cy="{y:.1f}" r="9" fill="{t["panel"]}" stroke="{nodecol[i]}" stroke-width="2.5"/>'
                    f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="3.5" fill="{nodecol[i]}"/></g>')
    add_grain(defs, body, W, H, mode, "pg")
    return frame(W, H, t, defs, body, "Targets: " + ", ".join(PLATFORM_ORDER) + ".", radius=16, cid="pc", bg=t["panel"])

# ------------------------------------------------------------------- divider
def divider(mode, seed="xwift", palette=None):
    t = THEMES[mode]; W, H = 960, 96
    I, V, N, E = cols(mode)
    r = art.rng(seed)
    c = palette or [I, V, N, E]
    if r.random() < 0.5: c = list(reversed(c))
    defs, body = [], []
    defs.append(f'<linearGradient id="dfade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.12" stop-color="#fff"/>'
                f'<stop offset="0.88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                f'<mask id="dm"><rect width="{W}" height="{H}" fill="url(#dfade)"/></mask>')
    fr = art.wave_frames(0, W, H / 2, 10 + r.random() * 8, 1.2 + r.random(), phase=r.random() * 6)
    dd, bb = art.ribbon("dv", None, 40, c, twist=3 + r.randint(0, 3), phase=r.random(), frames_in=fr, strands=3, shade=shade(mode), env_pow=0.35)
    defs.append(dd)
    fr2 = art.wave_frames(0, W, H / 2 + 4, 18, 0.8 + r.random(), phase=r.random() * 6)
    d2, b2 = art.ribbon("dv2", None, 14, list(reversed(c)), twist=2, frames_in=fr2, sheen=False, shade=0, opacity=0.5, env_pow=0.35)
    defs.append(d2)
    body.append(f'<g mask="url(#dm)">{b2}{bb}</g>')
    return svg_doc(W, H, "", f'<defs>{"".join(defs)}</defs>{"".join(body)}')

# ----------------------------------------------------------- project cards
ORG_PROJECTS = [
    ("01", "toolchain", "xwift", "Compiler and toolchain. Xwift's own fork of Swift and LLVM.", "ember"),
    ("02", "ui framework", "xwift-ui", "One UI framework for every Xwift target.", "violet"),
    ("03", "system apis", "xwift-system", "System APIs with one shape on every platform.", "ion"),
    ("04", "package manager", "xwift-pm", "Packages, dependencies and builds.", "pulse"),
]

def _illo(kind, x, y, w, h, mode, uid):
    I, V, N, E = cols(mode)
    defs, body = [], []
    if kind == "toolchain":   # layered bands: source descending through the stages
        for k, (c, ph) in enumerate([([E, N], 0.2), ([N, V], 0.9), ([V, I], 1.6)]):
            yy = y + 40 + k * 34
            dd, bb = art.ribbon(f"{uid}{k}", [(x - 20, yy + 50), (x + w * 0.35, yy - 50), (x + w * 0.6, yy + 70), (x + w + 20, yy - 20)],
                                (18, 34), c, twist=1.2, phase=ph, strands=1, shade=shade(mode), anim=art.enter(0.2 * k, dx=-12))
            defs.append(dd); body.append(bb)
    elif kind == "ui framework":  # floating panels
        for k, (dx, dy, rot, c1, c2) in enumerate([(0.30, 26, -8, V, I), (0.46, 48, 4, N, V), (0.62, 30, 12, I, V)]):
            px, py = x + w * dx, y + dy
            defs.append(f'<linearGradient id="{uid}p{k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
            body.append(f'<g transform="rotate({rot} {px+80} {py+55})" opacity="0.92">{art.enter(0.15*k, dy=10)}'
                        f'<rect x="{px}" y="{py}" width="160" height="110" rx="14" fill="url(#{uid}p{k})" fill-opacity="0.85"/>'
                        f'<rect x="{px+14}" y="{py+14}" width="54" height="6" rx="3" fill="#fff" fill-opacity="0.7"/>'
                        f'<rect x="{px+14}" y="{py+30}" width="96" height="6" rx="3" fill="#fff" fill-opacity="0.45"/>'
                        f'<rect x="{px+14}" y="{py+72}" width="40" height="22" rx="11" fill="#fff" fill-opacity="0.8"/></g>')
    elif kind == "system apis":  # arcs and nodes from one corner
        cx, cy = x + w + 10, y + h + 30
        for k, c in enumerate([I, V, I, N]):
            rr = 70 + k * 46
            defs.append(f'<linearGradient id="{uid}a{k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="0.15"/><stop offset="1" stop-color="{c}"/></linearGradient>')
            body.append(f'<path d="M{cx-rr} {cy} A{rr} {rr} 0 0 1 {cx} {cy-rr}" fill="none" stroke="url(#{uid}a{k})" stroke-width="{10-k*1.5}" stroke-linecap="round">{art.enter(0.15*k)}</path>')
            for a in (0.25, 0.55, 0.8):
                ang = math.pi + a * math.pi / 2
                nx, ny = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
                body.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4" fill="{c}"/>')
        body.append(art.flight(f"M{x+20} {y+150} C{x+w*0.3} {y+40} {x+w*0.6} {y+120} {x+w} {y+20}", I, 0.6))
    else:  # package manager: isometric cubes
        def cube(px, py, s, c1, c2, c3, k):
            h = s * 0.5
            top = f"M{px} {py-h}L{px+s*0.866} {py-h-h}L{px+s*1.732} {py-h}L{px+s*0.866} {py}Z"
            left = f"M{px} {py-h}L{px+s*0.866} {py}L{px+s*0.866} {py+s}L{px} {py+s-h}Z"
            right = f"M{px+s*0.866} {py}L{px+s*1.732} {py-h}L{px+s*1.732} {py+s-h}L{px+s*0.866} {py+s}Z"
            return (f'<g>{art.enter(0.12*k, dy=-14)}<path d="{top}" fill="{c1}"/><path d="{left}" fill="{c2}"/><path d="{right}" fill="{c3}"/>'
                    f'<path d="{top}{left}{right}" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="0.8"/></g>')
        s = 36; bx, by = x + w * 0.42, y + 80
        for k, (dx, dy) in enumerate([(0, -1.0), (-1, -0.5), (1, -0.5), (0, 0), (-1, 0.5), (1, 0.5), (0, 1.0)]):
            body.append(cube(bx + dx * s * 0.866, by + dy * s, s, N if k % 2 == 0 else E, V, N if k % 2 else E, k))
    return defs, body

def org_projects(mode):
    t = THEMES[mode]; W, H = 960, 600; g = 16
    cw, ch = (W - g) / 2, (H - g) / 2
    defs, body = [], []
    for i, (num, kind, repo, desc, col) in enumerate(ORG_PROJECTS):
        x = (i % 2) * (cw + g); y = (i // 2) * (ch + g)
        c = PAL[col] if not (mode == "dark" and col == "violet") else t["second"]
        cid = f"cc{i}"
        defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="16"/></clipPath>')
        fd, fb = art.fields(f"cf{i}", W, H, [(x + cw * 0.8, y + 30, 150, c, fop(mode) * 1.2), (x + 20, y + ch, 120, c, fop(mode) * 0.5)], blur=45)
        defs.append(fd)
        idefs, ibody = _illo(kind, x, y, cw, 170, mode, f"il{i}")
        defs += idefs
        body.append(f'<g clip-path="url(#{cid})"><rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="{t["panel"]}"/>{fb}{"".join(ibody)}'
                    f'<rect x="{x:.1f}" y="{y+150:.1f}" width="{cw:.1f}" height="{ch-150:.1f}" fill="url(#cardfade)"/></g>'
                    f'<rect x="{x+0.5:.1f}" y="{y+0.5:.1f}" width="{cw-1:.1f}" height="{ch-1:.1f}" rx="16" fill="none" stroke="{t["rule"]}"/>'
                    f'<text x="{x+28:.1f}" y="{y+196:.1f}" font-family="{MONO}" font-size="12" letter-spacing="0.8" fill="{c}">{num}  {kind.upper()}</text>'
                    f'<text x="{x+27:.1f}" y="{y+238:.1f}" font-family="{SANS}" font-size="34" font-weight="700" letter-spacing="-1.1" fill="{t["text"]}">{repo}</text>'
                    f'<text x="{x+28:.1f}" y="{y+268:.1f}" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{esc(desc)}</text>')
    defs.append(f'<linearGradient id="cardfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["panel"]}" stop-opacity="0"/>'
                f'<stop offset="0.35" stop-color="{t["panel"]}" stop-opacity="0.92"/><stop offset="1" stop-color="{t["panel"]}"/></linearGradient>')
    return svg_doc(W, H, "Projects: " + "; ".join(f"{r}, {k}" for _, k, r, _, _ in ORG_PROJECTS), f'<defs>{"".join(defs)}</defs>{"".join(body)}')

# --------------------------------------------------------------- footer band
def footer_band(mode, seed="xwift-org", caption="Write once. Run everything."):
    t = THEMES[mode]; W, H = 960, 300
    I, V, N, E = cols(mode)
    r = art.rng(seed)
    defs, body = [], []
    d, b = art.fields("ff", W, H, [(160, 300, 240, I, fop(mode)), (480, 330, 260, V, fop(mode)), (820, 300, 240, E, fop(mode)), (480, 60, 140, N, fop(mode) * 0.5)], blur=60)
    defs.append(d); body.append(b)
    cx, cy = W / 2, 118
    palette = [[I, V], [V, N], [N, E], [E, N], [V, I], [I, N], [N, V], [E, V]]
    for k in range(8):
        side = -1 if k % 2 == 0 else 1
        ex = W / 2 + side * (W / 2 + 40)
        ey = 90 + k * 26 + r.uniform(-10, 10)
        pts = [(ex, ey), (W / 2 + side * r.uniform(220, 360), ey + r.uniform(-90, 90)), (cx + side * r.uniform(80, 160), cy + r.uniform(-40, 60)), (cx + side * 30, cy)]
        dd, bb = art.ribbon(f"fr{k}", pts, (r.uniform(30, 60), 2), palette[k], twist=r.uniform(0.8, 1.8), phase=r.random(), opacity=0.85,
                            strands=1, shade=shade(mode), anim=art.enter(0.1 * k, dx=-side * 20))
        defs.append(dd); body.append(bb)
    add_grain(defs, body, W, H, mode, "fg")
    halo(defs, t, "fh")
    body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="90" ry="70" fill="url(#fh)"/>')
    bh = 64; bw = BIRD["viewBox"][2] / BIRD["viewBox"][3] * bh
    body.append(bird(cx - bw / 2, cy - bh / 2, bh, mode=mode)[0])
    body.append(f'<ellipse cx="{cx}" cy="226" rx="300" ry="44" fill="url(#fh)"/>')
    body.append(f'<text x="{cx}" y="222" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" letter-spacing="-0.8" fill="{t["text"]}">{esc(caption)}</text>')
    body.append(f'<text x="{cx}" y="252" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(seed)}</text>')
    return frame(W, H, t, defs, body, f"{caption} {seed}", radius=20, cid="fc")

# --------------------------------------------------------------- repo banner
def repo_banner(cfg, mode):
    t = THEMES[mode]; W, H = 960, 360
    I, V, N, E = cols(mode)
    name, tagline = cfg["name"], cfg["tagline"]
    r = art.rng(name)
    defs, body = [], []
    d, b = art.fields("bf", W, H, [(820, 40, 220, r.choice([I, V]), fop(mode)), (900, 340, 200, r.choice([E, N]), fop(mode)),
                                   (560, 200, 160, V, fop(mode) * 0.6), (60, 380, 160, I, fop(mode) * 0.5)], blur=60)
    defs.append(d); body.append(b)
    sets = [[E, N, V], [V, I], [N, E], [I, V, N], [E, V]]
    r.shuffle(sets)
    ox, oy = 290, 74  # wake starts right of the 'Xwift kind' label
    for k in range(5):
        ey = r.uniform(-30, H + 30)
        pts = [(ox, oy + k * 3), (ox + r.uniform(160, 300), oy + r.uniform(-80, 40)), (W * r.uniform(0.6, 0.8), ey + r.uniform(-80, 80)), (W + 40, ey)]
        w = (2 + k, r.uniform(40, 90) * (1 if k < 3 else 0.6))
        dd, bb = art.ribbon(f"br{k}", pts, w, sets[k], twist=r.uniform(0.8, 2.0), phase=r.random(), opacity=0.9,
                            strands=1 + (k % 2), shade=shade(mode), anim=art.enter(0.15 * k, dx=-24))
        defs.append(dd); body.append(bb)
    body.append(art.flight(f"M{ox} {oy} C{ox+200} {oy-60} {W*0.6} {oy+120} {W} {oy+40}", t["text"], 0.3))
    add_grain(defs, body, W, H, mode, "bg")
    defs.append(f'<linearGradient id="bshade" x1="0" x2="1"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="0.96"/>'
                f'<stop offset="0.5" stop-color="{t["bg"]}" stop-opacity="0.75"/><stop offset="0.7" stop-color="{t["bg"]}" stop-opacity="0"/></linearGradient>')
    body.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bshade)"/>')
    bsv, bw = bird(56, 52, 54, mode=mode)
    body.append(bsv)
    body.append(f'<text x="{56+bw+14:.0f}" y="88" font-family="{SANS}" font-size="20" font-weight="600" letter-spacing="-0.3" fill="{t["text"]}">Xwift'
                f'<tspan font-family="{MONO}" font-size="13" font-weight="400" fill="{t["muted"]}" dx="10">{esc(cfg.get("kind",""))}</tspan></text>')
    body.append(f'<text x="54" y="196" font-family="{SANS}" font-size="72" font-weight="700" letter-spacing="-2.6" fill="{t["text"]}">{esc(name)}</text>')
    body.append(f'<text x="56" y="236" font-family="{SANS}" font-size="21" letter-spacing="-0.2" fill="{t["muted"]}">{esc(tagline)}</text>')
    # platform chips on a translucent shelf
    plats = cfg.get("platforms", [])
    shelf_y = H - 76
    if not plats:
        return frame(W, H, t, defs, body, f"{name}. {tagline} Part of Xwift.", radius=16, cid="bc")
    body.append(f'<rect x="40" y="{shelf_y}" width="{W-80}" height="44" rx="22" fill="{t["panel"]}" fill-opacity="0.82" stroke="{t["rule"]}"/>')
    x = 64
    for i, p in enumerate(plats):
        st = p.get("status", "planned")
        cy_ = shelf_y + 22
        dot = (f'<circle cx="{x+6}" cy="{cy_}" r="4" fill="{t["accent"]}"/>' if st == "working" else
               f'<circle cx="{x+6}" cy="{cy_}" r="3.5" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>' if st == "in-progress" else
               f'<circle cx="{x+6}" cy="{cy_}" r="3.5" fill="none" stroke="{t["muted"]}" stroke-width="1.2"/>')
        body.append(f'<g>{fade_in(0.6+0.12*i, 0.4, 0.6+0.12*len(plats)+0.4)}{dot}'
                    f'<text x="{x+17}" y="{cy_+5}" font-family="{SANS}" font-size="14" fill="{t["text"] if st!="planned" else t["muted"]}">{esc(p["name"])}</text></g>')
        x += 17 + len(p["name"]) * 8.2 + 26
    lx = W - 64
    for txt, kind in reversed([("working", "working"), ("in progress", "in-progress"), ("planned", "planned")]):
        lx -= len(txt) * 6.6
        body.append(f'<text x="{lx:.0f}" y="{shelf_y+26}" font-family="{MONO}" font-size="11" fill="{t["muted"]}">{txt}</text>')
        cx_ = lx - 9; cy_ = shelf_y + 22
        body.append(f'<circle cx="{cx_:.0f}" cy="{cy_}" r="3.5" fill="{t["accent"]}"/>' if kind == "working" else
                    f'<circle cx="{cx_:.0f}" cy="{cy_}" r="3" fill="none" stroke="{t["accent"]}" stroke-width="1.4"/>' if kind == "in-progress" else
                    f'<circle cx="{cx_:.0f}" cy="{cy_}" r="3" fill="none" stroke="{t["muted"]}" stroke-width="1.2"/>')
        lx = cx_ - 20
    return frame(W, H, t, defs, body, f"{name}. {tagline} Part of Xwift.", radius=16, cid="bc")
