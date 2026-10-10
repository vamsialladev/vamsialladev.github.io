# Vamsi Alla · Portfolio

Personal portfolio site. Plain HTML and CSS, no build step.

## Before publishing: replace placeholders
Search all files for `YOUR-` and replace each one:

| Placeholder | Replace with |
|---|---|
| `YOUR-LINKEDIN` | Your LinkedIn profile ID |
| `YOUR-STREAMLIT-APP` | Your deployed Streamlit app name |
| `YOUR-VIDEO-LINK` | Your demo video link |
| `YOUR-NUMBER` | Your hybrid search accuracy |

Also:
- Write the **About** section in `index.html` in your own words, using only your real experience.
- Add your resume as `assets/Vamsi-Alla-Resume.pdf`.
- Optionally add a screenshot as `assets/hotel-assistant.png` (see the comment in the case study page).

## Link previews
`assets/og-home.png` and `assets/og-hotel-ops.png` are the images LinkedIn, Slack and X show when someone shares a link. After publishing, test them with the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/); it also refreshes LinkedIn's cached preview if you change the images. If your numbers change (e.g. after running hybrid search), update the case study image too.

## Preview locally
```bash
python -m http.server 8000
```
Open http://localhost:8000

## Publish on GitHub Pages
1. Create a public repo named exactly `vamsialladev.github.io` and push these files.
2. In the repo, open **Settings → Pages**. Set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site appears at `https://vamsialladev.github.io` within a few minutes.

## Connect your own domain
1. Buy the domain (Cloudflare Registrar or Namecheap, about $10–15/year).
2. In your domain's DNS settings, add:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | vamsialladev.github.io |

3. In **Settings → Pages → Custom domain**, enter your domain and save. GitHub adds a `CNAME` file to the repo for you; pull it before your next push (`git pull`).
4. After DNS updates (minutes to a few hours), tick **Enforce HTTPS**.
