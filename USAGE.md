# Xwift README templates

Two templates. One look: swift.org's, rebuilt for GitHub.

- `org/profile/` is the organization profile. It goes in the org's `.github` repository as `profile/README.md`, with `profile/assets/`.
- `repo/` is the repository template. `render.py` turns a TOML config into a README and its artwork for any Xwift repository.

The org is [xwift-org](https://github.com/xwift-org). This template system lives at [xwift-org/readme-template](https://github.com/xwift-org/readme-template).
The measured swift.org values behind every block are in [`swiftorg-spec.md`](swiftorg-spec.md).

## How it maps swift.org onto a README

GitHub strips CSS and web fonts from READMEs. So everything typographic or decorative is an SVG, and body copy stays Markdown.

- Every SVG is 980 units wide: one unit is one CSS pixel of swift.org's 980 px content column. At `width="100%"` the README column becomes that column, so sizes, gaps and radii keep swift.org's proportions.
- Each block has a light and a dark file, switched with `<picture>` and `prefers-color-scheme`. Block edges fade into GitHub's page colours (`#ffffff`, `#0d1117`), so stacked images read as one page.
- Text inside SVGs is outlined: glyph paths from Inter (with its Display optical size and dynamic tracking, standing in for SF Pro) and JetBrains Mono (for SF Mono), stored in `brand/glyphs.json`. No font is embedded or loaded.
- Links live in Markdown. Drawn navigation is decoration; the link row under the hero is the real navigation.

## Layout

```
brand/
  bird.json, bird-*.svg  the Xwift mark (line art), light and dark colours
  glyphs.json            outlined glyphs, advances and kerning (built by tools/build_glyphs.py)
  palette.json           Xwift brand palette
org/profile/
  profile.toml           every word of the org profile, and its structure
  README.md              generated
  assets/                generated: hero, intro, callout-*, code-*, swoop-*, section-*, closing (light and dark)
repo/
  render.py              entry point: org profile or repository README
  render_base.py         swift.org tokens (type, colour, spacing), outlined text, the Xwift mark
  art.py                 primitives: airbrushed ribbons, swoops, grain, icons
  artwork.py             compositions: hero, nav, intro, callout header, code card, swoop, closing band + footer, repo banner, platform cards
  examples/xwift/        sample: config, README.md, .github/assets/
tools/
  build_glyphs.py        rebuilds brand/glyphs.json (needs fonttools, uharfbuzz)
  shoot_swiftorg.py      reference screenshots of swift.org into refs/ (local only, never committed)
  computed_swiftorg.py   computed-style dump of swift.org into study/ (local only)
  shoot_github.py        screenshots a README as github.com renders it, light and dark
  preview_local.py       quick preview through the GitHub Markdown API
  shoot_svg.py           renders SVG blocks to PNG
```

## Org profile

1. Edit `org/profile/profile.toml`. Keep every claim true today; say "planned" for what is not built.
2. Render:

   ```sh
   python3 repo/render.py org --org xwift-org --out /path/to/xwift-org/.github/profile
   ```

   This writes `README.md` and `assets/` into the target folder. Without `--out` it writes into `org/profile/`.
3. Commit `profile/README.md` and `profile/assets/` to `xwift-org/.github`. The repository must be public.

The profile follows swift.org's home page: nav and hero (title, three-word tagline, button, caption, three cards, four chips, swoop), the 24 px intro, three callouts, a swoop, two more callouts, then Status and Contact, then the purple closing band and the footer.

## Repository README

1. Copy `repo/examples/xwift/xwift.toml` into the repository as `xwift.toml` and edit it.
2. Render:

   ```sh
   python3 /path/to/readme-template/repo/render.py repo xwift.toml
   ```

   It writes `README.md` next to the config, and the blocks into `assets_dir` (default `.github/assets`): `banner`, `section-*`, `platforms` and `closing`, light and dark. The banner's ribbons are seeded by the repository name.
3. `render.py` stops if a required key is missing or a placeholder is left.

### Config keys

| Key | Fills | Notes |
| --- | --- | --- |
| `name` | banner title (56 px) | Short. Lowercase repo names read best. |
| `kind` | banner button | `toolchain`, `tooling`, `library` ... |
| `tagline` | banner sub-text (32 px) | One sentence. |
| `description` | first Markdown paragraphs | Two short paragraphs at most. |
| `install` | Install section, `sh` code block | Real commands. |
| `usage`, `usage_lang` | Usage section | A real example. |
| `output` | Usage section, `text` block | Optional. Real output. |
| `platforms` | platform cards | `name`, `status` (`working`, `in-progress`, `planned`), `note`. Optional. |
| `platforms_text` | Platforms section | Used when `platforms` is empty. |
| `status`, `contributing`, `license` | their sections | Plain sentences. |
| `*_subtitle` | section subtitles | e.g. `install_subtitle = "Get the code. Build it."` Defaults are set in `render.py`. |
| `links` | link row and nav labels | `label`, `url`. Only links that resolve today. |
| `band` | closing band | Optional `title`, `subtitle`, `links`. |
| `org`, `assets_dir` | | Defaults `<org>`, `.github/assets`. |

## Voice

swift.org's: short, confident, declarative, plain words. One-word section titles with a five-to-seven word subtitle. Three-beat taglines. Paragraphs of 30 to 60 words. Write it fresh; never reuse swift.org's sentences.

## Rules

- Never use the Swift logo, the swift.org bird, any Apple logo, Apple fonts, or swift.org's image files. Artwork is drawn by `art.py`; the Xwift mark comes from `brand/`.
- Every claim is true today. Xwift is early: the fork is private, nothing is released, there is no website yet. Contact: vido.teodor10@gmail.com.
- Mention Swift only to describe what Xwift is built on.
- Keep this line at the end of every README:

  > Xwift is an independent project. It is not affiliated with or endorsed by Apple Inc. Swift is a trademark of Apple Inc.

## What GitHub cannot do

- No section background behind Markdown text. swift.org's tinted pillars (pale blue, peach) cannot sit behind body copy, so the colour lives in the hero, the swoops and the closing band.
- Body text is GitHub's 16 px in GitHub's font stack (SF Pro on Apple platforms, Segoe UI on Windows, the system sans elsewhere), not swift.org's 17 px.
- No hover states, no sticky translucent nav, no scroll-triggered swoops. Drawn nav and cards are not clickable; the Markdown link row is.
- Images stack with GitHub's 16 px paragraph gap, so every block starts and ends on the page colour.
- Animations run once when the image loads, not when it scrolls into view.
