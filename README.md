# vamsialla.com

The portfolio of Vamsi Alla, Senior Software Engineer: experience, the hotel operations case study and how I work.
Live at **https://vamsialla.com**.

## Stack
Plain HTML, CSS and a small amount of JavaScript, served by GitHub Pages. No framework, no build step, no
dependencies at runtime. `.nojekyll` turns off Jekyll so `.well-known/` is served.

| Path | What it is |
|---|---|
| `index.html`, `about.html`, `experience.html`, `projects.html`, `contact.html`, `privacy.html` | Public pages |
| `projects/hotel-ops-assistant.html` | Case study (keep the path: old links redirect here) |
| `notes.html`, `notes/*.html` | Notes, hidden until approved (`noindex`, not in nav or sitemap, no analytics) |
| `404.html` | Not-found page (root-relative paths, because it's served for any missing URL) |
| `data/projects.json` | The five engagement stages; the one place to change a project's status |
| `assets/style.css`, `assets/site.js` | The only stylesheet and script |
| `assets/fonts/` | Newsreader 500 (regular, italic) and Public Sans, self-hosted latin subsets |
| `assets/img/` | WebP screenshots with PNG/JPG fallbacks and 800 px variants |
| `videos/` | Demo video, poster and captions (made by `scripts/record_demo.py` in hotel-ops-assistant) |
| `.well-known/security.txt`, `robots.txt`, `sitemap.xml`, `CNAME` | Site metadata; `CNAME` is exactly `vamsialla.com` |

## Run it locally
```bash
python -m http.server 8000
```
Open http://localhost:8000. Analytics never count on localhost.

## Design tokens
All defined as custom properties at the top of `assets/style.css`.

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#F7F4EE` | `#111613` |
| `--surface` | `#FFFFFF` | `#18201C` |
| `--ink` | `#1C1F1D` | `#ECE8E0` |
| `--muted` | `#5B625E` | `#A3ABA6` |
| `--primary` | `#1E4636` | `#8CC4A5` |
| `--line` | `#E3DDD2` | `#26302B` |
| `--brass-text` (small text) | `#7A5C22` | `#D4B26A` |
| `--brass-decor` (lines, large text) | `#94702C` | `#D4B26A` |

Type: Newsreader 500 for headings, Public Sans for body at 18px / 1.65, 68ch reading width. Spacing on an 8px
scale, 12px card radius, 8px button radius. Theme follows the system, with a toggle remembered in `localStorage`
and applied before first paint.

## Targets
- WCAG AA contrast for every text pair in both themes (ratios are noted at the top of the stylesheet), one h1 per
  page, skip link, visible focus, keyboard-usable menu, alt text, captions and a transcript for the video.
- Lighthouse (mobile) 95+ for Performance, Accessibility, Best Practices and SEO on the public pages.
- A Content-Security-Policy meta tag on every page allows only this site, the self-hosted fonts and GoatCounter.
  Any new external script or font must be added to the CSP; inline scripts are allowed only by hash.
- CI (`.github/workflows/site-checks.yml`): HTML validation and a link check on every push and pull request.

## Analytics
GoatCounter (site code `vamsialla`), cookie-free and only on public pages. Nothing is counted on localhost or
`file://`, when the browser sends Do Not Track, or when `localStorage.skipgc` is set. To stop counting your own
visits, open `https://vamsialla.com/#toggle-goatcounter` once in each browser. Details on `privacy.html`.

## License
Code (HTML structure, CSS, JavaScript): MIT. Written content, the case study text, images, video and the resume:
© Vamsi Alla, all rights reserved.
