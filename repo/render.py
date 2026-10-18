#!/usr/bin/env python3
"""Render Xwift README assets.

  python3 render.py repo CONFIG.toml [--out DIR]   # banner, divider, footer SVGs + README.md for one repo
  python3 render.py org  [--org NAME] [--out DIR]  # org profile README + artwork

Standard library only (Python 3.11+ for tomllib). No fonts are embedded:
every SVG uses system font stacks. All artwork is generated in art.py and
artwork.py from the Xwift palette.
"""
import argparse, os, pathlib, sys, tomllib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from render_base import *  # noqa
import artwork

def platforms_table(plats):
    rows = ["| Platform | Status | Notes |", "| --- | --- | --- |"]
    for p in plats:
        rows.append(f'| {p["name"]} | {STATUS_LABEL.get(p.get("status","planned"))} | {p.get("note","")} |')
    return "\n".join(rows)

def links_line(links):
    return " &nbsp;·&nbsp; ".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in links)

def render_repo(cfg_path, out):
    cfg = tomllib.loads(pathlib.Path(cfg_path).read_text())
    out = pathlib.Path(out or pathlib.Path(cfg_path).parent); assets = out / cfg.get("assets_dir", ".github/assets")
    assets.mkdir(parents=True, exist_ok=True)
    for m in THEMES:
        (assets / f"banner-{m}.svg").write_text(artwork.repo_banner(cfg, m))
        (assets / f"divider-{m}.svg").write_text(artwork.divider(m, seed=cfg["name"]))
        (assets / f"footer-{m}.svg").write_text(artwork.footer_band(m, seed=cfg.get("org", "xwift") + "/" + cfg["name"], caption=cfg["tagline"]))
    rel = os.path.relpath(assets, out).replace(os.sep, "/")
    tpl = (pathlib.Path(__file__).parent / "README.template.md").read_text()
    vals = {
        "REPO_NAME": cfg["name"], "TAGLINE": cfg["tagline"], "DESCRIPTION": cfg["description"].strip(),
        "INSTALL": cfg["install"].strip(), "USAGE": cfg["usage"].strip(), "USAGE_LANG": cfg.get("usage_lang", "sh"),
        "OUTPUT": cfg.get("output", "").strip(),
        "PLATFORMS": platforms_table(cfg["platforms"]) if cfg.get("platforms") else cfg.get("platforms_text", "Not applicable."), "STATUS": cfg["status"].strip(),
        "CONTRIBUTING": cfg.get("contributing", "").strip(), "LICENSE": cfg.get("license", "TBD"),
        "LINKS": links_line(cfg.get("links", [])), "ASSETS": rel,
    }
    text = tpl
    for k, v in vals.items():
        text = text.replace("{{" + k + "}}", v)
    text = text.replace("{{ORG}}", cfg.get("org", "<org>"))
    if not vals["OUTPUT"]:
        text = text.replace("```text\n\n```\n", "")
    left = [line for line in text.splitlines() if "{{" in line]
    if left:
        sys.exit(f"unfilled placeholders: {left}")
    (out / "README.md").write_text(text)
    print(f"wrote {out/'README.md'} and {assets}/banner-{{light,dark}}.svg")

def render_org(org, out):
    out = pathlib.Path(out or ROOT / "org" / "profile"); a = out / "assets"; a.mkdir(parents=True, exist_ok=True)
    for m in THEMES:
        (a / f"hero-{m}.svg").write_text(artwork.org_hero(m))
        (a / f"platforms-{m}.svg").write_text(artwork.org_platforms(m))
        (a / f"projects-{m}.svg").write_text(artwork.org_projects(m))
        (a / f"divider-a-{m}.svg").write_text(artwork.divider(m, seed="get-started"))
        (a / f"divider-b-{m}.svg").write_text(artwork.divider(m, seed="community"))
        (a / f"footer-{m}.svg").write_text(artwork.footer_band(m, seed=org or "xwift"))
    src = ROOT / "org" / "profile" / "README.md"
    if org:
        (out / "README.md").write_text(src.read_text().replace("{{ORG}}", org))
    print(f"wrote org assets to {a}" + (f" and README for {org}" if org else ""))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("repo"); r.add_argument("config"); r.add_argument("--out")
    o = sub.add_parser("org"); o.add_argument("--org"); o.add_argument("--out")
    args = ap.parse_args()
    render_repo(args.config, args.out) if args.cmd == "repo" else render_org(args.org, args.out)
