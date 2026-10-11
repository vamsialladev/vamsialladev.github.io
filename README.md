# Vamsi Alla · Portfolio

Personal portfolio site. Plain HTML and CSS, no build step.

## Still to fill in
The live demo is at https://hotel-ops-assistant.streamlit.app. These are hidden in HTML comments until you do
them, so nothing looks broken:
- Write the **About** section in `index.html` in your own words, using only your real experience.

The case study's screenshots and GIF (`assets/hotel-assistant-*.png`, `.gif`) are real captures from the app,
copied from the project repo's `docs/images/`. The narrated demo video, its poster and captions
track (`videos/hotel-ops-demo.*`) are made by `scripts/record_demo.py` in the project repo from the live app.

## Link previews
`assets/og-home.png` and `assets/og-hotel-ops.png` are the images LinkedIn, Slack and X show when someone shares a link. After publishing, test them with the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/); it also refreshes LinkedIn's cached preview if you change the images. If the project's numbers change, regenerate `og-hotel-ops.png` (same layout, rendered with the site's fonts) and update the case study and home page stats.

## Preview locally
```bash
python -m http.server 8000
```
Open http://localhost:8000

## Publish on GitHub Pages
1. Create a public repo named exactly `vamsialla.com` and push these files.
2. In the repo, open **Settings → Pages**. Set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site appears at `https://vamsialla.com` within a few minutes.

## Connect your own domain
1. Buy the domain (Cloudflare Registrar or Namecheap, about $10–15/year).
2. In your domain's DNS settings, add:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | vamsialla.com |

3. In **Settings → Pages → Custom domain**, enter your domain and save. GitHub adds a `CNAME` file to the repo for you; pull it before your next push (`git pull`).
4. After DNS updates (minutes to a few hours), tick **Enforce HTTPS**.
