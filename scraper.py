"""Fetch every source, normalize the posts, and write data/news.json.

    python scraper.py          # scrape once and print a summary
"""

import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from dateutil import parser as dateparser

from sources import SOURCES
from topics import classify

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

DATA_FILE = Path(__file__).parent / "data" / "news.json"
USER_AGENT = "Mozilla/5.0 (compatible; ai-news-aggregator/1.0; personal use)"
TIMEOUT = 25
MAX_PER_SOURCE = 40
MAX_AGE_DAYS = 365

DATE_RE = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.? \d{1,2}, \d{4}\b"
    r"|\b\d{4}-\d{2}-\d{2}\b"
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def to_iso(value) -> str | None:
    """Parse any date-ish value into an ISO-8601 UTC string."""
    if not value:
        return None
    try:
        if isinstance(value, time.struct_time):
            dt = datetime(*value[:6], tzinfo=timezone.utc)
        else:
            dt = dateparser.parse(str(value))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (ValueError, OverflowError):
        return None


def day_to_iso(day: str) -> str | None:
    """A date with no time ("Sep 23, 2026"): use midday UTC so it shows as the same day in every time zone."""
    return to_iso(f"{day} 12:00")


def clean(text: str | None, limit: int = 280) -> str:
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + "…"


# --- One function per source kind --------------------------------------------

def scrape_rss(src: dict) -> list[dict]:
    feed = feedparser.parse(fetch(src["url"]))
    posts = []
    for e in feed.entries:
        posts.append({
            "title": clean(e.get("title"), 200),
            "url": e.get("link"),
            "date": to_iso(e.get("published_parsed") or e.get("updated_parsed")),
            "summary": clean(e.get("summary")),
            "tags": [t.get("term") for t in e.get("tags", [])[:3] if t.get("term")],
        })
    return posts


def scrape_html(src: dict) -> list[dict]:
    """Find article links on a listing page, then look near each one for a title and date.

    Sites without RSS lay their cards out differently, so rather than hard-coding
    CSS classes (which break on every redesign), walk up from each link until the
    surrounding card contains a date.
    """
    soup = BeautifulSoup(fetch(src["url"]), "html.parser")
    pattern = re.compile(src["link_pattern"])

    def article_url(a) -> str | None:
        href = a.get("href", "").split("?")[0].split("#")[0]
        return urllib.parse.urljoin(src["url"], href) if pattern.match(href) else None

    # The same post is often linked several times (nav menu, featured card, grid card).
    # Collect every occurrence, then keep the best title and any date we found.
    found: dict[str, dict] = {}
    for a in soup.find_all("a", href=True):
        url = article_url(a)
        if not url:
            continue
        post = found.setdefault(url, {"titles": [], "date": None, "order": len(found)})

        # Title candidates, best first: a heading inside the link, then labels, then the link text.
        heading = a.find(["h1", "h2", "h3", "h4"]) or a.find(class_=re.compile("title", re.I))
        if heading:
            post["titles"].append((0, heading.get_text(" ", strip=True)))
        for attr in ("aria-label", "title"):
            if a.get(attr):
                post["titles"].append((1, re.sub(r"^(Read|Learn more about)\s+", "", a[attr])))
        post["titles"].append((2, a.get_text(" ", strip=True)))

        # Climb to the enclosing card, but stop before a container that also holds
        # links to other posts (that would be the whole list, with other posts' dates).
        node = a
        for _ in range(5):
            if m := DATE_RE.search(node.get_text(" ", strip=True)):
                post["date"] = post["date"] or day_to_iso(m.group(0))
                break
            parent = node.parent
            if parent is None or any(article_url(x) not in (None, url) for x in parent.find_all("a", href=True)):
                break
            node = parent
            if h := node.find(["h1", "h2", "h3", "h4"]):
                post["titles"].append((0, h.get_text(" ", strip=True)))

    posts = []
    for url, p in sorted(found.items(), key=lambda kv: kv[1]["order"]):
        titles = [clean(DATE_RE.sub("", t), 200).strip(" ·|-") for _, t in sorted(p["titles"], key=lambda x: x[0])]
        # Skip labels like "FEATURED" or "Read more" that aren't real titles.
        titles = [t for t in titles if len(t) >= 8 and not t.isupper() and t.lower() not in ("read more", "learn more")]
        if titles:
            posts.append({"title": titles[0], "url": url, "date": p["date"], "summary": "", "tags": []})

    # Featured cards often show no date: open those few posts and read it from the article.
    for post in [p for p in posts if not p["date"]][:5]:
        post["date"] = article_date(post["url"])
    return posts


def article_date(url: str) -> str | None:
    try:
        soup = BeautifulSoup(fetch(url), "html.parser")
    except Exception:
        return None
    meta = soup.find("meta", property="article:published_time") or soup.find("meta", itemprop="datePublished")
    if meta and meta.get("content"):
        return to_iso(meta["content"])
    if t := soup.find("time"):
        if d := to_iso(t.get("datetime")) or to_iso(t.get_text(strip=True)):
            return d
    main = soup.find("main") or soup.body or soup
    m = DATE_RE.search(main.get_text(" ", strip=True))
    return day_to_iso(m.group(0)) if m else None


def scrape_hn(src: dict) -> list[dict]:
    since = int(time.time()) - src["days"] * 86400
    params = urllib.parse.urlencode({
        "query": src["query"],
        "optionalWords": src["query"],  # match ANY of the words, not all of them
        "tags": "story",
        "numericFilters": f"points>{src['min_points']},created_at_i>{since}",
        "hitsPerPage": 100,
    })
    data = json.loads(fetch(f"https://hn.algolia.com/api/v1/search?{params}"))
    word_re = re.compile(r"\b(" + "|".join(src["query"].split()) + r")\b", re.I)
    posts = []
    for h in data["hits"]:
        if not word_re.search(h.get("title") or ""):  # keep only titles that are actually about AI
            continue
        discussion = f"https://news.ycombinator.com/item?id={h['objectID']}"
        posts.append({
            "title": h["title"],
            "url": h.get("url") or discussion,
            "date": to_iso(h["created_at"]),
            "summary": "",
            "tags": [],
            "points": h.get("points", 0),
            "comments": h.get("num_comments", 0),
            "discussion": discussion,
        })
    posts.sort(key=lambda p: p["points"], reverse=True)
    return posts


SCRAPERS = {"rss": scrape_rss, "html": scrape_html, "hn": scrape_hn}


def scrape_source(src: dict) -> tuple[dict, list[dict]]:
    start = time.time()
    status = {"id": src["id"], "name": src["name"], "org": src["org"], "group": src["group"],
              "ok": True, "error": None, "count": 0}
    try:
        posts = [p for p in SCRAPERS[src["kind"]](src) if p.get("title") and p.get("url")]
    except Exception as e:  # one broken site must not break the page
        status.update(ok=False, error=f"{type(e).__name__}: {e}"[:200])
        return status, []

    cutoff = time.time() - MAX_AGE_DAYS * 86400
    posts = [p for p in posts if not p["date"] or dateparser.parse(p["date"]).timestamp() > cutoff]
    posts = posts[:MAX_PER_SOURCE]
    for p in posts:
        p.update(source=src["id"], source_name=src["name"], org=src["org"], group=src["group"])
        classify(p, src)
    status.update(count=len(posts), undated=sum(1 for p in posts if not p["date"]),
                  seconds=round(time.time() - start, 1))
    return status, posts


def scrape_all(previous: dict | None = None) -> dict:
    """Scrape everything in parallel. Keeps first-seen times so undated posts can still be sorted."""
    first_seen = {p["url"]: p.get("first_seen") for p in (previous or {}).get("posts", [])}
    now = datetime.now(timezone.utc).isoformat()

    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(scrape_source, SOURCES))

    # Feeds sometimes fail or come back empty for a moment. Keep that source's
    # previous posts rather than making them vanish until the next refresh.
    old_by_source: dict[str, list[dict]] = {}
    for p in (previous or {}).get("posts", []):
        old_by_source.setdefault(p["source"], []).append(p)
    for status, source_posts in results:
        if not source_posts and old_by_source.get(status["id"]):
            source_posts.extend(old_by_source[status["id"]])
            status.update(stale=True, count=len(source_posts))

    posts, seen_urls = [], set()
    for _, source_posts in results:
        for p in source_posts:
            if p["url"] in seen_urls:
                continue
            seen_urls.add(p["url"])
            p["first_seen"] = first_seen.get(p["url"]) or now
            posts.append(p)

    posts.sort(key=lambda p: p["date"] or p["first_seen"], reverse=True)
    return {"updated": now, "sources": [s for s, _ in results], "posts": posts}


def load() -> dict | None:
    try:
        return json.loads(DATA_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    tmp.replace(DATA_FILE)  # atomic, so the server never reads a half-written file


if __name__ == "__main__":
    import editions

    data = scrape_all(load())
    save(data)
    print(f"{editions.update(data)} daily editions updated")
    for s in data["sources"]:
        mark = ("~" if s.get("stale") else "✓") if s["ok"] else "✗"
        extra = s["error"] if not s["ok"] else f"{s['count']} posts ({s.get('undated', 0)} undated, {s.get('seconds')}s)"
        print(f"{mark} {s['name']:<24} {extra}")
    print(f"\n{len(data['posts'])} posts → {DATA_FILE}")
