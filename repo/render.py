#!/usr/bin/env python3
"""Render Xwift READMEs in the swift.org style.

  python3 repo/render.py org  [--org NAME] [--out DIR]   org profile from org/profile/profile.toml
  python3 repo/render.py repo CONFIG.toml [--out DIR]     repository README from a TOML config

Every block is an SVG 980 units wide (swift.org's content column) in a light and a dark variant,
switched with <picture> and prefers-color-scheme. Text inside the SVGs is outlined from
brand/glyphs.json, so nothing depends on fonts. Body copy stays Markdown.
Standard library only (Python 3.11+).
"""
import argparse, os, pathlib, sys, tomllib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import artwork
from render_base import ROOT, THEMES, esc

DISCLAIMER = ("<sub>Xwift is an independent project. It is not affiliated with or endorsed by Apple Inc. "
              "Swift is a trademark of Apple Inc.</sub>")

def picture(rel, name, alt, link=None):
    img = (f'<picture>\n    <source media="(prefers-color-scheme: dark)" srcset="{rel}/{name}-dark.svg">\n'
           f'    <source media="(prefers-color-scheme: light)" srcset="{rel}/{name}-light.svg">\n'
           f'    <img src="{rel}/{name}-light.svg" width="100%" alt="{esc(alt)}">\n  </picture>')
    if link: img = f'<a href="{link}">{img}</a>'
    return f'<p align="center">\n  {img}\n</p>\n'

def link_row(links):
    return ('<p align="center">\n  ' + " &nbsp;·&nbsp;\n  ".join(f'<a href="{l["url"]}">{esc(l["label"])}</a>' for l in links)
            + "\n</p>\n") if links else ""

def anchor(i): return f'<a id="{i}"></a>\n'

def write(assets, name, fn):
    for m in THEMES:
        (assets / f"{name}-{m}.svg").write_text(fn(m))

# ---------------------------------------------------------------- org profile
def render_org(org, out):
    cfg = tomllib.loads((ROOT / "org" / "profile" / "profile.toml").read_text())
    org = org or cfg.get("org", "xwift-org")
    out = pathlib.Path(out or ROOT / "org" / "profile"); a = out / "assets"; a.mkdir(parents=True, exist_ok=True)
    h = dict(cfg["hero"]); h["cards"] = [(c["icon"], c["title"], c["text"]) for c in h["cards"]]
    md = []
    write(a, "hero", lambda m: artwork.hero(m, m, h))
    md.append(picture("./assets", "hero", " ".join(h["title"]) + " " + h["sub"] + " " + h["caption"] + "."))
    md.append(link_row(cfg["links"]))
    write(a, "intro", lambda m: artwork.intro(m, cfg["intro"]))
    md.append(anchor("overview") + picture("./assets", "intro", cfg["intro"]))
    section = 1
    for c in cfg["callouts"]:
        if c.get("section", 1) != section:
            section = c["section"]
            write(a, f"swoop-{section - 1}", lambda m, s=section: artwork.swoop(m, "cool" if s == 2 else "warm", seed=1.3 * s, tint="pillar2" if s == 2 else None))
            md.append(picture("./assets", f"swoop-{section - 1}", ""))
        write(a, f"callout-{c['id']}", lambda m, c=c: artwork.callout_head(m, c["title"], c["subtitle"]))
        md.append(anchor(c["id"]) + picture("./assets", f"callout-{c['id']}", f'{c["title"]}. {c["subtitle"]}'))
        md.append(c["body"].strip() + "\n")
        if c.get("code"):
            write(a, f"code-{c['id']}", lambda m, c=c: artwork.code_card(m, c["code"], c.get("lang", "swift")))
            md.append(picture("./assets", f"code-{c['id']}", c["code"].strip()))
    for key, aid in (("status", "status"), ("contact_section", "contact")):
        s = cfg[key]
        write(a, f"section-{aid}", lambda m, s=s: artwork.callout_head(m, s["title"], s["subtitle"]))
        md.append(anchor(aid) + picture("./assets", f"section-{aid}", f'{s["title"]}. {s["subtitle"]}'))
        md.append(s["body"].strip() + "\n")
    f = cfg["footer"]; cols = [(c.get("head"), c["items"]) for c in f["columns"]]
    write(a, "closing", lambda m: artwork.closing(m, m, cfg["band"], {"columns": cols, "note": f["note"]}))
    md.append(picture("./assets", "closing", f'{cfg["band"]["title"]}. {cfg["band"]["subtitle"]} ' + " · ".join(cfg["band"]["links"]),
                      link=f'mailto:{cfg["contact"]}'))
    md.append(DISCLAIMER + "\n")
    text = "\n".join(md).replace("{{ORG}}", org)
    (out / "README.md").write_text(text)
    print(f"wrote {out / 'README.md'} and {a}/ for {org}")

# ---------------------------------------------------------------- repository README
SECTIONS = [  # (anchor, title, subtitle key, default subtitle)
    ("install", "Install", "install_subtitle", "Get the code. Build it."),
    ("usage", "Usage", "usage_subtitle", "Run it."),
    ("platforms", "Platforms", "platforms_subtitle", "Where it runs today."),
    ("status", "Status", "status_subtitle", "What works, and what does not yet."),
    ("contributing", "Contributing", "contributing_subtitle", "Small changes. Green CI."),
    ("license", "License", "license_subtitle", "Terms of use."),
]

def render_repo(cfg_path, out):
    cfg = tomllib.loads(pathlib.Path(cfg_path).read_text())
    for k in ("name", "tagline", "description", "install", "usage", "status"):
        if not str(cfg.get(k, "")).strip(): sys.exit(f"missing config key: {k}")
    org = cfg.get("org", "<org>")
    out = pathlib.Path(out or pathlib.Path(cfg_path).parent)
    assets = out / cfg.get("assets_dir", ".github/assets"); assets.mkdir(parents=True, exist_ok=True)
    rel = os.path.relpath(assets, out).replace(os.sep, "/")
    sub = lambda s: s.replace("{{ORG}}", org)
    md = []
    write(assets, "banner", lambda m: artwork.repo_banner(m, m, cfg))
    md.append(picture(rel, "banner", f'{cfg["name"]}. {cfg["tagline"]}'))
    md.append(link_row(cfg.get("links", [])))
    md.append(sub(cfg["description"].strip()) + "\n")
    body = {
        "install": f'```sh\n{sub(cfg["install"].strip())}\n```\n',
        "usage": f'```{cfg.get("usage_lang", "sh")}\n{sub(cfg["usage"].strip())}\n```\n'
                 + (f'\n```text\n{cfg["output"].strip()}\n```\n' if cfg.get("output", "").strip() else ""),
        "platforms": None, "status": sub(cfg["status"].strip()) + "\n",
        "contributing": cfg.get("contributing", "").strip() + "\n", "license": cfg.get("license", "Not chosen yet.") + "\n",
    }
    for aid, title, skey, sdef in SECTIONS:
        if aid == "contributing" and not cfg.get("contributing", "").strip(): continue
        write(assets, f"section-{aid}", lambda m, t=title, s=cfg.get(skey, sdef): artwork.callout_head(m, t, s))
        md.append(anchor(aid) + picture(rel, f"section-{aid}", f'{title}. {cfg.get(skey, sdef)}'))
        if aid == "platforms":
            if cfg.get("platforms"):
                write(assets, "platforms", lambda m: artwork.platform_cards(m, cfg["platforms"]))
                md.append(picture(rel, "platforms", "Platforms"))
                md.append("| Platform | Status | Notes |\n| --- | --- | --- |\n" + "\n".join(
                    f'| {p["name"]} | {p.get("status", "")} | {p.get("note", "")} |' for p in cfg["platforms"]) + "\n")
            else:
                md.append(cfg.get("platforms_text", "Not applicable.") + "\n")
        else:
            md.append(body[aid])
    band = cfg.get("band", {"title": "Follow Along", "subtitle": "Xwift is early. This is the time to join.",
                            "links": ["vido.teodor10@gmail.com", f"github.com/{org}"]})
    cols = [(None, [l["label"] for l in cfg.get("links", [])][:5] or ["README"]),
            ("Repository", ["Install", "Usage", "Status", "Contributing"]),
            ("Contact", ["vido.teodor10@gmail.com", f"github.com/{org}"])]
    write(assets, "closing", lambda m: artwork.closing(m, m, band, {"columns": cols, "note": [
        "Xwift is in early development.", "Xwift is not affiliated with or endorsed by Apple Inc."]}))
    md.append(picture(rel, "closing", f'{band["title"]}. {band["subtitle"]}', link=cfg.get("contact_link", "mailto:vido.teodor10@gmail.com")))
    md.append(DISCLAIMER + "\n")
    text = "\n".join(md)
    if "{{" in text: sys.exit("unfilled placeholders: " + ", ".join(l for l in text.splitlines() if "{{" in l))
    (out / "README.md").write_text(text)
    print(f"wrote {out / 'README.md'} and {assets}/")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("repo"); r.add_argument("config"); r.add_argument("--out")
    o = sp.add_parser("org"); o.add_argument("--org"); o.add_argument("--out")
    args = ap.parse_args()
    render_repo(args.config, args.out) if args.cmd == "repo" else render_org(args.org, args.out)
