# Xwift README templates

Two templates. One look.

- `org/profile/` is the organization profile. It goes in the org's `.github` repository as `profile/README.md`, with `profile/assets/`.
- `repo/` is the repository template. `render.py` turns a TOML config into a banner and a README for any Xwift repository.

The org is [xwift-org](https://github.com/xwift-org). This template system lives at [xwift-org/readme-template](https://github.com/xwift-org/readme-template).

## Layout

```
brand/
  bird.json            vector trace of the Xwift bird, light and dark colors
  bird-light.svg       standalone bird, light logo colors
  bird-dark.svg        standalone bird, dark logo colors
  palette.json         Ink, Ion, Violet, Pulse, Ember, Paper
org/profile/
  README.md            org profile, with {{ORG}} placeholders
  assets/              hero, platforms, dividers, projects, footer (light and dark)
repo/
  README.template.md   repository README with {{PLACEHOLDERS}}
  render.py            entry point: renders artwork and README.md from a config
  render_base.py       palette, themes, font stacks, the bird
  art.py               primitives: ribbons, flight paths, color fields, grain
  artwork.py           compositions: hero, platform strip, dividers, project cards, footer band, repo banner
  examples/xwift/      sample: config, README.md, .github/assets/
inspo/                 swift.org screenshots used for study
preview-*.png          GitHub-like previews
```

## Org profile

1. Pick the org name.
2. Render the README with the name filled in:

   ```sh
   python3 repo/render.py org --org <org> --out /path/to/<org>/.github/profile
   ```

   This writes `README.md` and `assets/` into the target folder. Without `--org`, only the SVGs are regenerated in `org/profile/assets/`.
3. Check the project names in `README.md` and in `ORG_PROJECTS` in `render.py`. `xwift-ui`, `xwift-system` and `xwift-pm` are placeholders until those repositories exist.
4. Commit `profile/README.md` and `profile/assets/` to `<org>/.github`. The repository must be public.

## Repository README

1. Copy `repo/examples/xwift/xwift.toml` into the repository as `xwift.toml` (or keep it next to `render.py`) and edit it.
2. Render:

   ```sh
   python3 /path/to/repo/render.py repo xwift.toml
   ```

   It writes `README.md` next to the config and, into `assets_dir` (default `.github/assets`), `banner`, `divider` and `footer` SVGs in light and dark. The artwork is seeded by the repository name, so every repository gets its own composition in the same style.
3. `render.py` stops if any placeholder is left unfilled.

### Config keys

| Key | Fills | Notes |
| --- | --- | --- |
| `name` | `{{REPO_NAME}}`, banner title | Short. Lowercase repo names read best. |
| `kind` | banner, top right | `toolchain`, `ui framework`, `library` ... |
| `tagline` | `{{TAGLINE}}`, banner subtitle | One sentence. |
| `description` | `{{DESCRIPTION}}` | Markdown. Two short paragraphs at most. |
| `install` | `{{INSTALL}}` | Shell, copied from real docs. |
| `usage`, `usage_lang` | `{{USAGE}}` | A real example. `usage_lang` sets the code fence. |
| `output` | `{{OUTPUT}}` | Optional. Real output of the usage example. Omitted when empty. |
| `platforms` | `{{PLATFORMS}}`, banner chips | `name`, `status` (`working`, `in-progress`, `planned`), `note`. Optional. |
| `platforms_text` | `{{PLATFORMS}}` | Used when `platforms` is empty. |
| `status` | `{{STATUS}}` | Plain sentences. What runs, where, and what does not yet. |
| `contributing` | `{{CONTRIBUTING}}` | Markdown list. |
| `license` | `{{LICENSE}}` | |
| `links` | `{{LINKS}}` | `label`, `url`. Only links that resolve today. |
| `org` | `{{ORG}}` | Optional. Defaults to `<org>`. |
| `assets_dir` | `{{ASSETS}}` | Default `.github/assets`. |

## Design rules

- System font stacks only. No font files are embedded. Apple platforms show SF; others fall back to Segoe UI, Helvetica or Arial.
- Light and dark variants through `<picture>` and `prefers-color-scheme`.
- Artwork is generated, never traced: tapered ribbons that turn over (the back face is a shade darker), fine strands along each ribbon, wing-like flight paths that grow out of the bird, blurred color fields, and a light grain.
- Motion is quiet. Ribbons slide into place once. A soft sheen travels along them, and dotted flight paths drift. Nothing starts hidden, so the first frame and the last frame both read.
- Ember is the accent. Violet, Ion and Pulse mark the other projects. Ink and Paper are the ground.
- Copy is terse and literal. Code blocks come from real docs and real output.
- Links live in markdown, outside images.

## Trademark

Xwift borrows the feel of swift.org, not its trade dress.

- Do not use the Swift logo, the swift.org bird, its ribbon shapes, its orange gradient, its wording or its layout.
- Use the Xwift bird and the Xwift palette.
- Mention Swift only to describe what Xwift is built on.
- Keep this line at the end of every README:

  > Xwift is an independent project. It is not affiliated with or endorsed by Apple Inc. Swift is a trademark of Apple Inc.

## Previews

The previews render each README through the GitHub Markdown API, wrapped in GitHub's markdown CSS, and screenshot it in headless Chrome. They show what GitHub will show, minus GitHub's own page chrome.
