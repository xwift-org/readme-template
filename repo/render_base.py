"""Shared constants and helpers for the Xwift README renderer."""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
PAL = json.loads((BRAND / "palette.json").read_text())
BIRD = json.loads((BRAND / "bird.json").read_text())

SANS = ("-apple-system, BlinkMacSystemFont, &quot;SF Pro Display&quot;, &quot;Segoe UI&quot;, "
        "&quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif")
MONO = "&quot;SF Mono&quot;, ui-monospace, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace"

THEMES = {
    "light": dict(bg="#FBF8F3", panel="#FFFFFF", text=PAL["ink"], muted="#5A5F73",
                  rule="#E7E1D6", chip="#F4EFE6", accent=PAL["ember"], second=PAL["violet"]),
    "dark":  dict(bg=PAL["ink"], panel="#11162A", text="#F4EFE6", muted="#9AA0B8",
                  rule="#232A44", chip="#161C33", accent=PAL["ember"], second="#9C85FF"),
}
PLATFORM_ORDER = ["macOS", "Windows", "Linux", "Android", "iOS", "Web"]
STATUS_LABEL = {"working": "working", "in-progress": "in progress", "planned": "planned"}

def esc(s): return html.escape(str(s), quote=True)

def bird(x, y, h, anim=True, delay=0.0, mode="light"):
    col = BIRD["colors_dark"] if mode == "dark" else BIRD["colors"]
    vw, vh = BIRD["viewBox"][2], BIRD["viewBox"][3]
    s = h / vh
    sw = 0.9 / s  # thicken the traced line by ~1px at display size
    a = ""
    if anim:
        # glide in from the left once; the final frame is the resting logo
        a = (f'<animateTransform attributeName="transform" type="translate" additive="sum" '
             f'values="-18 0;-18 0;0 0" keyTimes="0;{min(delay/1.6,0.5):.2f};1" dur="1.6s" fill="freeze"/>'
             "")
    return (f'<g><g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})">'
            f'<path d="{BIRD["violet"]}" fill="{col["violet"]}" fill-rule="evenodd" stroke="{col["violet"]}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<path d="{BIRD["orange"]}" fill="{col["orange"]}" fill-rule="evenodd" stroke="{col["orange"]}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'</g>{a}</g>'), vw * s

def svg_doc(w, h, label, body, bg=None, radius=16, stroke=None):
    frame = ""
    if bg:
        frame = f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{radius}" fill="{bg}"' + (f' stroke="{stroke}"' if stroke else "") + "/>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{frame}{body}</svg>\n')

def fade_in(delay, dur=0.5, total=None):
    """Kept for compatibility. Text stays static so every frame reads, even the first."""
    return ""

