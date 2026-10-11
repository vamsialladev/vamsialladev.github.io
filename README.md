# Vamsi Alla · Portfolio

Personal portfolio at **https://vamsialla.com**. Plain HTML, CSS and a little JavaScript on GitHub Pages: no
framework and no build step.

## Pages
| Page | File |
|---|---|
| Home | `index.html` |
| Experience | `experience.html` (matches `assets/Vamsi-Alla-Resume.pdf`) |
| Projects | `projects.html` |
| Hotel assistant case study | `projects/hotel-ops-assistant.html` (keep this path: old links redirect here) |
| About, with "How I work" and the privacy note | `about.html` |
| Contact | `contact.html` |
| Notes draft (not linked, `noindex`, no analytics) | `notes.html` |
| Not found | `404.html` |

## Changing things
- **Project status:** edit `data/projects.json` (status `Live`, `Next` or `Planned`). Home and Projects both
  render the five stages from it; nothing else needs to change.
- **Styles:** every color, space and type size is a custom property at the top of `assets/style.css`. Light and
  dark themes follow the system setting, with a manual toggle remembered in `localStorage`.
- **Video:** `videos/hotel-ops-demo.mp4`, its poster (`.jpg`) and captions (`.vtt`) are made by
  `scripts/record_demo.py` in the hotel-ops-assistant repo. Keep the paths.
- **Images:** `assets/img/*.webp` with `.png`/`.jpg` fallbacks; `assets/og-*.png` are the 1200×630 link previews.

## Analytics
GoatCounter (site code `vamsialla`), cookie-free, on public pages only (not the Notes draft or 404). Nothing is
counted on localhost or `file://`, when the browser sends Do Not Track, or when `localStorage.skipgc` is set.
To stop counting your own visits, open `https://vamsialla.com/#toggle-goatcounter` once in each browser.

## Still to do by hand
- Write the **About** paragraph in `about.html` (replace the marked placeholder).
- Approve the **Notes** draft, then add it to the nav and the sitemap and remove `noindex`.

## Domain
`CNAME` contains `vamsialla.com`. DNS is at Spaceship (GitHub Pages A/AAAA records, `www` CNAME and the
verification TXT record); HTTPS is enforced.
