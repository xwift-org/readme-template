"""Original Xwift artwork: ribbons, flight paths, color fields.

Every shape is generated here from the Xwift palette. Nothing is traced.
"""
import hashlib, math, random

def rng(seed):
    return random.Random(int(hashlib.sha256(str(seed).encode()).hexdigest()[:12], 16))

def _bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    x = u*u*u*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t*t*t*x3
    y = u*u*u*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t*t*t*y3
    dx = 3*u*u*(x1-x0) + 6*u*t*(x2-x1) + 3*t*t*(x3-x2)
    dy = 3*u*u*(y1-y0) + 6*u*t*(y2-y1) + 3*t*t*(y3-y2)
    n = math.hypot(dx, dy) or 1
    return x, y, -dy/n, dx/n

def bezier_frames(pts, n=72):
    return [_bez(pts, i / n) for i in range(n + 1)]

def wave_frames(x0, x1, yc, amp, periods, phase=0.0, n=140):
    out = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        a = 2 * math.pi * periods * t + phase
        y = yc + amp * math.sin(a)
        dx = (x1 - x0); dy = amp * 2 * math.pi * periods * math.cos(a)
        m = math.hypot(dx, dy)
        out.append((x, y, -dy / m, dx / m))
    return out

def ribbon(uid, pts, width, colors, twist=1.0, phase=0.3, opacity=1.0,
           sheen=True, edge=None, n=72, anim=None, shade=0.22, strands=0, strand_color=None, frames_in=None, env_pow=0.55):
    """A tapered, twisting ribbon along a cubic bezier.

    width can be a number or a (start, end) pair. The signed half-width follows
    cos(twist*pi*t + phase), so the band folds over itself like a turning ribbon.
    """
    left, right, mid, signs, frames = [], [], [], [], []
    w0, w1 = (width, width) if not isinstance(width, tuple) else width
    fr = frames_in or bezier_frames(pts, n)
    n = len(fr) - 1
    if pts is None:
        pts = [(fr[0][0], fr[0][1]), None, None, (fr[-1][0], fr[-1][1])]
    for i in range(n + 1):
        t = i / n
        x, y, nx, ny = fr[i]
        env = math.sin(math.pi * t) ** env_pow  # taper both ends
        w = (w0 + (w1 - w0) * t) * env * math.cos(twist * math.pi * t + phase) / 2
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w)); mid.append((x, y))
        signs.append(w < 0); frames.append((x, y, nx, ny, abs((w0 + (w1 - w0) * t) * env / 2)))
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in left) + "L" + "L".join(f"{x:.1f} {y:.1f}" for x, y in reversed(right)) + "Z"
    (x0, y0), (x3, y3) = pts[0], pts[3]
    stops = "".join(f'<stop offset="{i/(len(colors)-1):.2f}" stop-color="{c}"/>' for i, c in enumerate(colors))
    defs = f'<linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x3:.0f}" y2="{y3:.0f}">{stops}</linearGradient>'
    body = f'<path d="{d}" fill="url(#{uid})"/>'
    if sheen:
        defs += (f'<linearGradient id="{uid}s" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x3:.0f}" y2="{y3:.0f}">'
                 f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.45" stop-color="#fff" stop-opacity="0.38"/>'
                 f'<stop offset="0.6" stop-color="#fff" stop-opacity="0"/>'
                 f'<animate attributeName="x1" values="{x0-300:.0f};{x0+300:.0f};{x0-300:.0f}" dur="11s" repeatCount="indefinite"/>'
                 f'<animate attributeName="x2" values="{x3-300:.0f};{x3+300:.0f};{x3-300:.0f}" dur="11s" repeatCount="indefinite"/>'
                 f'</linearGradient>')
        body += f'<path d="{d}" fill="url(#{uid}s)"/>'
    if shade:
        # the back face of the ribbon, where it has turned over, is a shade darker
        runs, cur = [], []
        for i, neg in enumerate(signs):
            if neg: cur.append(i)
            elif cur: runs.append(cur); cur = []
        if cur: runs.append(cur)
        for r in runs:
            if len(r) < 2: continue
            a, b = max(r[0] - 1, 0), min(r[-1] + 1, n)
            seg = "M" + "L".join(f"{left[i][0]:.1f} {left[i][1]:.1f}" for i in range(a, b + 1)) + "L" + "L".join(f"{right[i][0]:.1f} {right[i][1]:.1f}" for i in range(b, a - 1, -1)) + "Z"
            body += f'<path d="{seg}" fill="#0A0E1F" fill-opacity="{shade}"/>'
    if strands:
        sc = strand_color or f"url(#{uid})"
        for k in range(1, strands + 1):
            f = (k / (strands + 1) - 0.5) * 2.4
            pts_ = [(x + nx * hw * f, y + ny * hw * f) for x, y, nx, ny, hw in frames]
            body += f'<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts_) + f'" fill="none" stroke="{sc}" stroke-opacity="0.55" stroke-width="0.9"/>'
    if edge:
        body += f'<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in left) + f'" fill="none" stroke="{edge}" stroke-opacity="0.55" stroke-width="0.8"/>'
    a = anim or ""
    return defs, f'<g opacity="{opacity}">{body}{a}</g>'

def enter(delay=0.0, dx=0, dy=0, dur=1.4):
    """One-pass slide into place; the resting frame is the final design."""
    total = delay + dur
    k = delay / total
    # translate only: a renderer that shows the first frame still shows every shape
    return (f'<animateTransform attributeName="transform" type="translate" values="{dx} {dy};{dx} {dy};0 0" '
            f'keyTimes="0;{k:.3f};1" keySplines="0 0 1 1;0.2 0.7 0.2 1" calcMode="spline" dur="{total:.2f}s" fill="freeze"/>')

def fields(uid, W, H, blobs, blur=60):
    """Layered abstract color fields: big soft discs under a blur."""
    defs = f'<filter id="{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>'
    body = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" opacity="{o}"/>' for x, y, r, c, o in blobs)
    return defs, f'<g filter="url(#{uid})">{body}</g>'

def flight(d, color, opacity=0.5, dash="2 7", dur=7, width=1.2):
    """A dotted flight path that keeps moving slowly."""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-dasharray="{dash}"><animate attributeName="stroke-dashoffset" '
            f'values="0;-90" dur="{dur}s" repeatCount="indefinite"/></path>')

def grain(uid, opacity=0.06):
    return (f'<filter id="{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>'
            f'<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 {opacity} 0"/></filter>')
