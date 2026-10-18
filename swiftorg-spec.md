# swift.org design spec, as measured

Measured on 18 Oct 2026 (Europe/Bratislava) from `https://www.swift.org/` and its stylesheet
`/assets/stylesheets/new-stylesheets/application.css` (86 KB), with computed styles read in headless Chrome
at a 1280 px viewport, light and dark (`tools/computed_swiftorg.py`, raw dump in `study/computed-home.json`,
not published). Reference screenshots are in `refs/` (local only; swift.org's images are never copied or published).

What the Xwift templates take from this: layout, proportions, type scale, spacing, colours, radii, rhythm and the
*style* of the artwork. What they do not take: the Swift logo, swift.org's image files, its fonts or its sentences.

## 1. Type

| Role | Selector | Size / line height | Weight | Colour light / dark | Xwift glyph style |
| --- | --- | --- | --- | --- | --- |
| Body | `body` | 17 px / 1.6 (27.2) | 400 | `#051416` / `#ffffff` | `text-400` |
| Hero title | `.title-0` (`#what-is-swift h1`) | 56 / 67.2 (1.2), centred, margin-bottom 30 | 600 | `#3d3d3d` / `#ffffff` | `display-600` |
| Hero sub-text | `.sub-text h2` | 32 / 51.2, margin 20 0 60 | 400 | `#3d3d3d` / `#ffffff` | `display-400` |
| Install button | `.hero-content > a` | 35 / 42, padding 15 81, radius 43 | 400 | `#fff` on `linear-gradient(to bottom right, #ff7f00, #f05238)` | `display-400` |
| Button caption | `.hero-content > p` | 17 / 27.2, margin-top 11, opacity .66 | 500 | `#3d3d3d` / `#dedede` | `text-500` |
| "Create using Swift" | `#what-is-swift h2` | 32 / 51.2, margin 70 0 29 | 400 | `#051416` / `#fff` | `display-400` |
| Card title | `.primary-links .title` | 24 / 38.4 | 600 | `#801a1a` / `#fff` | `text-600` |
| Card text | `.primary-links .subtitle` | 14 / 19.6 | 400 | same | `text-400` |
| Chip | `.secondary-links .title` | 14 / 22.4 | 400 | same | `text-400` |
| Pillar intro | `.pillar-intro` | 24 / 34.8 (1.45), centred, 720 px measure | 400 | `#051416` / `#fff` | `mid-400` |
| Section title | `.title-1` / `.callout-title` | 48 / 57.6, margin -4 0 3 | 500 | `#051416` / `#fff` | `display-500` |
| Section subtitle | `.callout-subtitle` (`.title-2` at 24 px) | 24 / 28.8, margin-bottom 22 | 500 | same | `mid-500` |
| Callout body | `.callout-text.body` | 17 / 26.01 (1.53) | 400 | same | Markdown |
| Code | `pre.highlight` / `code` | 14 / 21 | 400 | `#051416` / `#fff` | `mono-400` |
| Nav item | `.navigation-items li a` | 19 px, span padding 12 15, radius 36 | 400 | `#3d3d3d` / `#fff` | `text-400` |
| Footer heading | `footer h3` | 19.89 / 23.87 (1.17em) | 700 | `#fca76c` | `text-700` |
| Footer link | `footer nav ul li a` | 14 / 22.4, padding .35em 0 | 400 | `#ebecf0` | `text-400` |
| Mobile (≤768 px) | `.title-0` 40, `.title-1` 32 / 1.33, hero h1 32 / 1.33 | | | | |

- Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif`
  (SF Pro on Apple platforms). Code: `"SF Mono", ui-monospace, Menlo, Consolas, Monaco, "Courier New", monospace`.
- `letter-spacing` is `0` everywhere; SF Pro's optical tracking does the work. Xwift outlines Inter with Inter's
  dynamic tracking `-0.0223 + 0.185·e^(-0.1745·size)` em (−0.022 em at 56 px, −0.013 em at 17 px), and uses the
  `opsz` axis (14 for text, 24 mid, 32 display = Inter Display), which tracks SF Pro Text / Display closely.
  JetBrains Mono stands in for SF Mono. Both fonts are OFL 1.1 and are outlined, never embedded.

## 2. Colour

| Token | Light | Dark |
| --- | --- | --- |
| Page | `#ffffff` | `#000000` |
| Text | `#051416` | `#ffffff` |
| Hero background (`--homepage-hero-bg`) | `linear-gradient(179deg, #fac685 3%, #fbdab0 87%, #ffffff 100%)` | `linear-gradient(180deg, #144173 0%, #141228 68%, #144173 99%)` |
| Pillar 1 (`--homepage-pillar-1-bg`) | `linear-gradient(to bottom, #ffffff 0%, #d9f2ff 75%, #fff3d8 90%)` | `linear-gradient(179deg, #144173 1%, #000000 57%, #350839 88%, #df6b40 99%)` |
| Pillar 2 | `linear-gradient(to top, #e4937f 0%, #fdd9a1 72%, #fff3d8 100%)` | `linear-gradient(0deg, #ffac64 0, #df6b40 100%)` |
| Pillar 3 (Open Source) | `linear-gradient(180deg, #e4937f 0%, #a268c1 36%, #4b3773 100%)` | `linear-gradient(180deg, #ffac64 0%, #a268c1 28%, #4b3773 100%)` |
| Quick-link cards | `rgba(255,177,100,.9)`, text `#801a1a` | `#23344a`, text `#ffffff` |
| Nav bar | `rgba(255,255,255,.5)`, blur 20, shadow `0 1px 2px rgba(0,0,0,.05)` | `rgba(0,0,0,.3)`, no shadow |
| Nav selected | `rgba(230,150,80,.9)` | `rgb(221,93,67)` |
| Code block | `rgba(255,255,255,.5)`, border `1px #d5d5d5` | `#111727`, border `1px #575757` |
| Link with arrow | `#384fea` | `#1ec1fd` |
| Footer | `#1e162e`, text `#ebecf0`, headings `#fca76c` | same |
| Install page | `linear-gradient(0deg, #f6b391 0%, #f8ce6e 92%)` | `linear-gradient(0deg, #ff8115 0%, #b7451b 92%)` |
| Get Started hero | `linear-gradient(-16deg, #c49db2 1%, #7959d3 70%)` | same |
| Cards on inner pages | `rgba(255,255,255,.9)` / secondary `#ececec` | `rgba(35,52,74,.9)` / `#384461` |
| Grain | `noise.png` at opacity .04 over every section | same |

Syntax (light / dark): comments `#707f8c` / `#7f8c98`, keywords `#ad3da4` / `#ff79b3`, strings `#d12f1b` / `#ff8170`,
numbers `#272ad8` / `#d9c97c`, types `#703daa` / `#dabaff`, project names `#2d6469` / `#78c2b3`, `.n` `#b181ec`.

## 3. Space and shape

- Content column: `max-width: 980px` (`.callout`, `.content-wrapper`, quick links, inner-page `.content`). Nav wrapper 1234 px with 20 px side padding.
- Hero `#what-is-swift`: padding-top 72, padding-bottom 8vw (102 px at 1280); 1135 px tall at 1280. Content starts at 18vw.
  Title top at 302 px, sub-text at 467, button 578 (256 × 72), caption 661, "Create" 758, cards 838 (313 × 128, gap 20, padding 25, radius 36,
  icon 40 × 40, gap 12), chips 986 (46 px tall, padding 12, gap 15, radius 36).
- Pillar 1: padding 11.88vw 0 16.88vw (152 / 216 px). Pillar intro: padding 4vw 0 32, max-width 720.
- Callout: margin 2.5em auto (42.5 px), padding 1em (17 px), grid `2.2fr 3.2fr`, gap 40 (`.reverse` flips columns). Stacks to one column at ≤1024 px.
- Code block: padding 28, radius 20, 1 px border.
- Pillar 2: padding .94vw 0 12.5vw. Pillar 3: padding 5vw 0 40; callout max-width 760, links 17 px white, underline at 50% opacity, offset 2, 14 px apart.
- Footer: padding 6rem 3rem 3rem 3.5em (96 / 48 / 48 / 59.5), container 980, 4 columns, nav margin-bottom 5em; logo 36 px tall.
- Radii in use: 22 px (25×, inner-page cards, code boxes), 20 px (code, Get Started boxes), 36 px (nav pills, quick links), 43 px (button), 10 px (blog code).
- Shadows: almost none. Nav `0 1px 2px rgba(0,0,0,.05)`; blog dropdown `0 2px 5px rgba(0,0,0,.15)`.

## 4. Artwork and motion

- Hero: six stacked canvases (`purple-swoop`, `white-swoop-1`, `orange-swoop-top`, `orange-swoop-bottom`, `white-swoop-2`, `bird`), 1248 × 1116,
  57vw wide, animated with anime.js: the ribbons draw in and the bird lands. Ribbons are airbrushed: wide, twisting bands with soft cores,
  sprayed grainy edges, white highlights; palette pink / yellow-orange / white over the peach gradient.
- Section swoops (`swoop-0/1/2`): wide horizontal bands of violet, orange, pink, yellow and white strands rising left to right, translated 50% over the next section,
  faded in when scrolled into view.
- Xwift redraws this style from scratch in vector: `repo/art.py` builds each ribbon from offset strands around a spline, with a soft highlight stripe,
  a darker edge, a haze, a displacement-noise spray and 4–7% generated grain. Motion: ribbons glide in once (SMIL, ~2 s) and stay.
  No swift.org image is hotlinked, traced or copied, and there is no bird head: the Xwift mark sits in the nav and footer.

## 5. Page structure

| Page | Order |
| --- | --- |
| Home | nav · hero (title-0, sub-text, Install button, caption, "Create using Swift", 3 cards, 4 chips) · swoop-0 · pillar 1 (intro, Fast, Expressive, Safe) · swoop-1 · pillar 2 (Interoperable, Adaptable) · swoop-2 · pillar 3 (Open Source + 2 links) · footer |
| Install | peach gradient hero "Install Swift" + OS tabs · numbered steps in white 22 px-radius code boxes · editor cards · SDK bundles · development snapshots |
| Get Started | violet hero · "Installing Swift" · "Using Swift" card grid · "Go Further" image cards |
| Documentation | redirects to docs.swift.org (DocC) |
| Community | swoop hero · centred title card · forum categories grid · "How we work" · "Contribute to Swift" grid · "Follow Swift" icon row |
| Packages | text page · "Package Ecosystem" card grid · "Create Your Own" · "Advanced Search" |
| Blog | swoop strip · "Latest Swift News" featured card (22 px radius, 880:382 image) · category cards · post list cards with grey pills |

Voice: short declarative sentences, plain words, three-beat taglines ("Fast. Expressive. Safe."), headings of one word with a
five-to-seven word subtitle, paragraphs of 30–60 words.

## 6. Mapping onto a GitHub README

- One SVG unit = one swift.org CSS pixel of the 980 px column. GitHub's README column is 797–880 px of content, so blocks render at 0.81–0.9×.
  At that width swift.org itself uses its single-column callout layout (≤1024 px), which is what the README uses: title + subtitle, body, then code.
- Body copy is Markdown at GitHub's 16 px (swift.org: 17 px; at 0.81–0.9× scale the ratio to the headings is within ~10%).
  On Apple platforms GitHub's font stack also resolves to SF Pro, the same face swift.org uses.
- Light/dark: `<picture>` with `prefers-color-scheme`, as GitHub supports. Block edges fade to GitHub's page colours (`#ffffff`, `#0d1117`)
  so stacked images read as one page.
