"""Drawing primitives for the swift.org-style artwork, drawn from scratch.

swift.org paints its hero and section swoops as airbrushed ribbons: wide bands that twist,
made of fine strands, with sprayed, grainy edges. These functions build that look in vector form:
a ribbon is a bundle of offset strands around a spline, with a translucent body underneath,
a speckle filter on the edges and 4% film grain over the section (swift.org's noise.png opacity).
"""
import math, random

def catmull(points, n=140):
    """Sample a Catmull-Rom spline through points. Returns [(x, y)] of length ~n."""
    pts = [points[0]] + list(points) + [points[-1]]
    segs = len(points) - 1; per = max(2, n // segs); out = []
    for i in range(segs):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for k in range(per):
            t = k / per; t2 = t * t; t3 = t2 * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(points[-1])
    return out

def frame(c):
    """Cumulative length (normalised) and unit normals along a polyline."""
    L = [0.0]
    for a, b in zip(c, c[1:]): L.append(L[-1] + math.dist(a, b))
    tot = L[-1] or 1; s = [l / tot for l in L]; nrm = []
    for i in range(len(c)):
        a = c[max(0, i - 1)]; b = c[min(len(c) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nrm.append((-dy / d, dx / d))
    return s, nrm, tot

def poly(pts, close=False):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")

def taper(s, a=0.12, b=0.18):
    """0 at both ends, 1 in the middle, eased."""
    u = min(1.0, s / a) if a else 1.0; v = min(1.0, (1 - s) / b) if b else 1.0
    return math.sin(u * math.pi / 2) * math.sin(v * math.pi / 2)

def ribbon(uid, points, width, grad, *, twists=0.0, phase=0.0, strands=26, seed=1,
           body_opacity=0.82, strand_opacity=(0.18, 0.55), highlight="#ffffff", shade=None,
           ends=(0.10, 0.16), n=150, reveal=None, speckle=True, pinch=0.35, hi=0.22, haze=0.0, scatter=0.16):
    """One airbrushed ribbon.

    points: spline control points. width: full width in px at the widest.
    grad: [(offset, colour)] laid along the ribbon's start->end direction.
    twists: how many half-turns the band makes (the width pinches to an edge and the face flips).
    reveal: (begin, dur) seconds to draw the ribbon in along its length, once.
    Returns (defs, body).
    """
    rnd = random.Random(seed)
    c = catmull(points, n); s, nrm, tot = frame(c)
    def hw(i):
        t = s[i]; tw = abs(math.cos(math.pi * (twists * t + phase))) if twists else 1.0
        return 0.5 * width * taper(t, *ends) * (pinch + (1 - pinch) * tw)
    def face(i):
        return 1 if not twists or math.cos(math.pi * (twists * s[i] + phase)) >= 0 else -1
    left = [(c[i][0] + nrm[i][0] * hw(i), c[i][1] + nrm[i][1] * hw(i)) for i in range(len(c))]
    right = [(c[i][0] - nrm[i][0] * hw(i), c[i][1] - nrm[i][1] * hw(i)) for i in range(len(c))]
    x0, y0 = c[0]; x1, y1 = c[-1]
    gid = f"{uid}-g"
    defs = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}">'
            + "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in grad) + "</linearGradient>")
    def band(o0, o1):
        a = [(c[i][0] + nrm[i][0] * hw(i) * o0, c[i][1] + nrm[i][1] * hw(i) * o0) for i in range(len(c))]
        b = [(c[i][0] + nrm[i][0] * hw(i) * o1, c[i][1] + nrm[i][1] * hw(i) * o1) for i in range(len(c))]
        return poly(a + b[::-1], True)
    parts = []
    if haze:
        defs += (f'<filter id="{uid}-hz" x="-20%" y="-40%" width="140%" height="180%">'
                 f'<feGaussianBlur stdDeviation="{width * 0.22:.1f}"/></filter>')
        parts.append(f'<path d="{poly(left + right[::-1], True)}" fill="url(#{gid})" fill-opacity="{haze}" filter="url(#{uid}-hz)" transform="scale(1)"/>')
    parts.append(f'<path d="{poly(left + right[::-1], True)}" fill="url(#{gid})" fill-opacity="{body_opacity}"/>')
    # airbrushed volume: a bright stripe near one edge, a deeper tone along the other
    parts.append(f'<path d="{band(0.25, 0.85)}" fill="{highlight}" fill-opacity="{hi:.2f}" filter="url(#{uid}-soft)"/>')
    parts.append(f'<path d="{band(0.45, 0.70)}" fill="{highlight}" fill-opacity="{hi * 1.2:.2f}" filter="url(#{uid}-soft)"/>')
    if shade:
        parts.append(f'<path d="{band(-1.0, -0.45)}" fill="{shade}" fill-opacity="0.30" filter="url(#{uid}-soft)"/>')
    # the back face of each twist, a shade darker, like a turned-over band
    if twists and shade:
        seg = []; segs = []
        for i in range(len(c)):
            if face(i) < 0: seg.append(i)
            elif seg: segs.append(seg); seg = []
        if seg: segs.append(seg)
        for sg in segs:
            if len(sg) < 2: continue
            parts.append(f'<path d="{poly([left[i] for i in sg] + [right[i] for i in sg[::-1]], True)}" fill="{shade}" fill-opacity="0.28"/>')
    # fine strands: lighter and darker hairlines along the band
    sw = max(0.6, width / strands * 0.55)
    for k in range(strands):
        o = -1 + 2 * (k + rnd.random() * 0.8) / strands
        pts = [(c[i][0] + nrm[i][0] * hw(i) * o, c[i][1] + nrm[i][1] * hw(i) * o) for i in range(0, len(c), 2)]
        col = highlight if rnd.random() < 0.55 else f"url(#{gid})"
        op = rnd.uniform(*strand_opacity) * (1.15 - abs(o) * 0.5)
        parts.append(f'<path d="{poly(pts)}" fill="none" stroke="{col}" stroke-width="{sw * rnd.uniform(0.5, 1.4):.2f}" '
                     f'stroke-opacity="{min(op, 0.9):.2f}" stroke-linecap="round"/>')
    flt = f' filter="url(#{uid}-spk)"' if speckle else ""
    defs += (f'<filter id="{uid}-soft" x="-10%" y="-10%" width="120%" height="120%">'
             f'<feGaussianBlur stdDeviation="{max(1.5, width * 0.06):.1f}"/></filter>')
    if speckle:
        # sprayed edge: blur a little, then scatter the pixels with fine noise
        defs += (f'<filter id="{uid}-spk" x="-8%" y="-8%" width="116%" height="116%">'
                 f'<feGaussianBlur in="SourceGraphic" stdDeviation="{max(0.8, width * 0.02):.1f}" result="b"/>'
                 f'<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="{seed}" result="n"/>'
                 f'<feDisplacementMap in="b" in2="n" scale="{max(6, width * scatter):.1f}" xChannelSelector="R" yChannelSelector="G"/>'
                 f'</filter>')
    anim = ""
    if reveal:
        # glide in along the ribbon's direction and brighten, once. No masks: they render unreliably in <img>.
        b, d = reveal; dx = (x1 - x0); dy = (y1 - y0); k = 40 / (math.hypot(dx, dy) or 1)
        kt = f"0;{b / (b + d):.3f};1"
        anim = (f'<animateTransform attributeName="transform" type="translate" values="{-dx * k:.1f} {-dy * k:.1f};{-dx * k:.1f} {-dy * k:.1f};0 0" '
                f'keyTimes="{kt}" dur="{b + d:.2f}s" calcMode="spline" keySplines="0 0 1 1;0.25 0.1 0.25 1" fill="freeze"/>'
                f'<animate attributeName="opacity" values="0.15;0.15;1" keyTimes="{kt}" dur="{b + d:.2f}s" fill="freeze"/>')
    return defs, f'<g>{anim}<g{flt}>' + "".join(parts) + "</g></g>"

def wave(x0, x1, y, amp, k, phase, n=8):
    """Control points for a gentle horizontal S-wave."""
    return [(x0 + (x1 - x0) * i / (n - 1), y + amp * math.sin(k * i / (n - 1) * 2 * math.pi + phase)) for i in range(n)]

def grain(uid, w, h, opacity=0.04, freq=0.85):
    """swift.org lays noise.png at 4% over every section. Same idea, generated."""
    d = (f'<filter id="{uid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{freq}" '
         f'numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.6 -0.35"/></filter>')
    return d, f'<rect width="{w}" height="{h}" filter="url(#{uid})" opacity="{opacity}"/>'

def rrect(x, y, w, h, r, attrs=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" {attrs}/>'

# ---------------------------------------------------------------- icons (original, 24-unit grid, stroked)
ICONS = {
    "apps": '<rect x="3" y="4" width="13" height="10" rx="1.6"/><path d="M7 18h5M9.5 14v4"/><rect x="16" y="8" width="5.5" height="11" rx="1.3"/>',
    "web": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.4 3.8 5.2 3.8 8.5s-1.2 6.1-3.8 8.5c-2.6-2.4-3.8-5.2-3.8-8.5S9.4 5.9 12 3.5z"/>',
    "terminal": '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M7 10l3 2.5L7 15M12.5 15.5H17"/>',
    "chip": '<rect x="6.5" y="6.5" width="11" height="11" rx="1.5"/><path d="M9.5 3.5v3M14.5 3.5v3M9.5 17.5v3M14.5 17.5v3M3.5 9.5h3M3.5 14.5h3M17.5 9.5h3M17.5 14.5h3"/>',
    "box": '<path d="M12 3.5l7.5 4v9L12 20.5l-7.5-4v-9z"/><path d="M4.5 7.5L12 11.5l7.5-4M12 11.5v9"/>',
    "arrow": '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 12h7M12.5 8.8L15.7 12l-3.2 3.2"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3.8 7l8.2 6 8.2-6"/>',
}

def icon(name, x, y, size, color, sw=1.6):
    s = size / 24
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" fill="none" stroke="{color}" stroke-width="{sw / s * s:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')
