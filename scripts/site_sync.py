"""Keep every page in step with data/site.json: the nav and More menu, the footer pages, the Home cards and latest
notes, the Notes list, sitemap.xml and feed.xml. Standard library only.

    python scripts/site_sync.py          # rewrite the shared blocks, sitemap.xml and feed.xml
    python scripts/site_sync.py --check  # exit 1 if anything is out of date (used in CI)

Shared blocks sit between markers like <!--s:nav--> ... <!--/s:nav--> in the HTML.
"""

import html
import json
import re
import sys
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
URL = DATA["url"]
SECTIONS = [s for s in DATA["sections"] if s["published"]]
NOTES = sorted(DATA["notes"], key=lambda n: n["date"], reverse=True)
CHEVRON = ('<svg class="chev" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
           'stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>')


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def month_year(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%B %Y")


def long_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def section_of(path: str) -> str | None:
    """Which section a page belongs to, for aria-current."""
    for s in DATA["sections"]:
        if s["url"] == path:
            return s["id"]
    if path.startswith("projects/"):
        return "projects"
    if path.startswith("notes/"):
        return "notes"
    return None


# ---------- blocks ----------
def link(root: str, s: dict, active: str | None) -> str:
    current = ' aria-current="page"' if s["id"] == active else ""
    return f'<a href="{root}{s["url"]}"{current}>{esc(s["title"])}</a>'


def nav(root: str, active: str | None) -> str:
    main = "".join(f"<li>{link(root, s, active)}</li>" for s in SECTIONS if s["nav"] == "main")
    more = [s for s in SECTIONS if s["nav"] == "more"]
    if not more:
        return main
    has_current = any(s["id"] == active for s in more)
    items = "".join(f"<li>{link(root, s, active)}</li>" for s in more)
    return (f'{main}<li class="more{" current" if has_current else ""}">'
            f'<span class="more-title" aria-hidden="true">More</span>'
            f'<button class="more-btn" type="button" aria-expanded="false" aria-controls="more-menu">More{CHEVRON}</button>'
            f'<ul id="more-menu" class="more-menu">{items}</ul></li>')


def footer_pages(root: str) -> str:
    return "".join(f'<li><a href="{root}{s["url"]}">{esc(s["title"])}</a></li>' for s in SECTIONS if s["nav"] == "more")


def threads(root: str) -> str:
    cards = sorted((s for s in SECTIONS if s.get("card")), key=lambda s: s["card"]["n"])
    return "".join(
        f'<li><a class="card thread" href="{root}{s["url"]}"><span class="thread-n">{s["card"]["n"]:02d}</span>'
        f'<span class="thread-label">{esc(s["card"]["label"])}</span>'
        f'<span class="thread-headline">{esc(s["card"]["headline"])}</span><span class="thread-arrow" aria-hidden="true">→</span></a></li>'
        for s in cards
    )


def note_card(root: str, n: dict, heading: str = "h3") -> str:
    return (f'<li data-category="{esc(n["category"])}"><a class="card note-card" href="{root}{n["url"]}">'
            f'<span class="note-meta">{esc(n["category"])} · {month_year(n["date"])}</span>'
            f'<{heading}>{esc(n["title"])}</{heading}><p>{esc(n["subtitle"])}</p><span class="arrow-link">Read →</span></a></li>')


def latest_notes(root: str, limit: int = 2) -> str:
    return "".join(note_card(root, n) for n in NOTES[:limit])


def notes_list(root: str) -> str:
    used = [c for c in DATA["note_categories"] if any(n["category"] == c for n in NOTES)]
    chips = "".join(f'<li><button class="chip" type="button" aria-pressed="false" data-filter="{esc(c)}">{esc(c)}</button></li>'
                    for c in used)
    return (f'<div class="chips" role="group" aria-label="Filter notes by category"><ul>'
            f'<li><button class="chip" type="button" aria-pressed="true" data-filter="">All</button></li>{chips}</ul></div>'
            f'<ul class="note-list" data-notes>{"".join(note_card(root, n, "h2") for n in NOTES)}</ul>'
            f'<p class="small notes-empty" role="status" aria-live="polite"></p>')


BLOCKS = {"nav": nav, "footer-pages": lambda root, active: footer_pages(root),
          "threads": lambda root, active: threads(root), "latest-notes": lambda root, active: latest_notes(root),
          "notes-list": lambda root, active: notes_list(root)}


def wrap(name: str, inner: str) -> str:
    return f"<!--s:{name}-->{inner}<!--/s:{name}-->"


# ---------- files ----------
def sitemap() -> str:
    urls = [s["url"] for s in SECTIONS if s["id"] != "home"] + DATA["sitemap_extra"] + [n["url"] for n in NOTES]
    rows = [f"  <url><loc>{URL}/</loc><lastmod>{DATA['updated']}</lastmod></url>"]
    rows += [f"  <url><loc>{URL}/{u}</loc><lastmod>{DATA['updated']}</lastmod></url>" for u in urls]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def rfc822(iso: str) -> str:
    return format_datetime(datetime.fromisoformat(iso).replace(hour=12, tzinfo=timezone.utc))


def feed() -> str:
    items = "".join(
        f"""
    <item>
      <title>{esc(n["title"])}</title>
      <link>{URL}/{n["url"]}</link>
      <guid isPermaLink="true">{URL}/{n["url"]}</guid>
      <pubDate>{rfc822(n["date"])}</pubDate>
      <category>{esc(n["category"])}</category>
      <description>{esc(n["subtitle"])}</description>
    </item>"""
        for n in NOTES
    )
    built = rfc822(NOTES[0]["date"]) if NOTES else rfc822(DATA["updated"])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Notes | Vamsi Alla</title>
    <link>{URL}/notes.html</link>
    <description>Short write-ups on building software and AI that holds up: what worked, what didn't, and the numbers behind it.</description>
    <language>en-us</language>
    <lastBuildDate>{built}</lastBuildDate>
    <atom:link href="{URL}/feed.xml" rel="self" type="application/rss+xml"/>{items}
  </channel>
</rss>
"""


def sync_page(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    root = "/" if rel == "404.html" else "../" * rel.count("/")
    active = section_of(rel)
    text = path.read_text(encoding="utf-8")
    for name, render in BLOCKS.items():
        text = re.sub(rf"<!--s:{name}-->.*?<!--/s:{name}-->", lambda m: wrap(name, render(root, active)), text, flags=re.S)
    return text


def validate() -> list[str]:
    """Problems with sitemap.xml and feed.xml: well-formed XML, required RSS 2.0 fields, absolute URLs, every
    sitemap URL exists, and no unpublished section linked from any page, the sitemap or the feed."""
    import xml.etree.ElementTree as ET
    from email.utils import parsedate_to_datetime

    problems = []
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(ROOT / "sitemap.xml").getroot()
    if tree.tag != "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset":
        problems.append("sitemap: root is not <urlset>")
    for loc in tree.findall("s:url/s:loc", ns):
        url = loc.text or ""
        if not url.startswith(URL + "/"):
            problems.append(f"sitemap: not absolute: {url}")
        path = url[len(URL) + 1:] or "index.html"
        if not (ROOT / path).exists():
            problems.append(f"sitemap: missing file for {url}")
    for lastmod in tree.findall("s:url/s:lastmod", ns):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod.text or ""):
            problems.append(f"sitemap: bad lastmod {lastmod.text}")
    rss = ET.parse(ROOT / "feed.xml").getroot()
    channel = rss.find("channel")
    if rss.tag != "rss" or rss.get("version") != "2.0" or channel is None:
        problems.append("feed: not RSS 2.0")
    else:
        for tag in ("title", "link", "description"):
            if not (channel.findtext(tag) or "").strip():
                problems.append(f"feed: channel has no {tag}")
        if channel.find("{http://www.w3.org/2005/Atom}link[@rel='self']") is None:
            problems.append("feed: no atom:link rel=self")
        for item in channel.findall("item"):
            for tag in ("title", "link", "guid", "pubDate", "description"):
                if not (item.findtext(tag) or "").strip():
                    problems.append(f"feed: item without {tag}")
            if not (item.findtext("link") or "").startswith(URL + "/"):
                problems.append(f"feed: link not absolute: {item.findtext('link')}")
            try:
                parsedate_to_datetime(item.findtext("pubDate"))
            except (TypeError, ValueError):
                problems.append(f"feed: bad pubDate {item.findtext('pubDate')}")
    hidden = [s["url"] for s in DATA["sections"] if not s["published"]]
    texts = {"sitemap.xml": (ROOT / "sitemap.xml").read_text(encoding="utf-8"),
             "feed.xml": (ROOT / "feed.xml").read_text(encoding="utf-8")}
    for page in [*ROOT.glob("*.html"), *ROOT.glob("projects/*.html"), *ROOT.glob("notes/*.html")]:
        texts[page.relative_to(ROOT).as_posix()] = page.read_text(encoding="utf-8")
    for name, text in texts.items():
        for url in hidden:
            if re.search(rf'["/]{re.escape(url)}["#?]|{re.escape(URL)}/{re.escape(url)}', text):
                problems.append(f"{name}: links to unpublished {url}")
        if name.endswith(".html") and 'type="application/rss+xml"' not in text:
            problems.append(f"{name}: no RSS link in the head")
    return problems


def main(check: bool) -> int:
    if "--validate" in sys.argv:
        problems = validate()
        for p in problems:
            print(p)
        print("sitemap.xml and feed.xml valid" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    outputs = {ROOT / "sitemap.xml": sitemap(), ROOT / "feed.xml": feed()}
    for page in sorted([*ROOT.glob("*.html"), *ROOT.glob("projects/*.html"), *ROOT.glob("notes/*.html")]):
        outputs[page] = sync_page(page)
    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if check:
        for p in stale:
            print("out of date:", p.relative_to(ROOT).as_posix())
        print("site in sync" if not stale else "run: python scripts/site_sync.py")
        return 1 if stale else 0
    for p in stale:
        p.write_text(outputs[p], encoding="utf-8", newline="\n")
        print("updated", p.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
