"""Build the static site for GitHub Pages (or any static host).

    python build.py restore https://you.github.io/ai-wire/   # fetch the live data first
    python build.py                                         # scrape, then write site/

GitHub Actions starts every run on a blank machine, so `restore` downloads the
previous posts and daily archive from the published site. That keeps "first
seen" times and the archive growing without committing data to the repo.

Output (site/):
    index.html                        the page, switched to static mode
    logos/                            company logos
    data/news.json                    latest posts from every source
    data/editions/index.json          list of days in the archive
    data/editions/YYYY-MM-DD.json     one day's posts (used by "This week")
    data/editions/raw/YYYY-MM-DD.json the stored form, read back by `restore`
"""

import json
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

import editions
import scraper

ROOT = Path(__file__).parent
SITE = ROOT / "site"


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": scraper.USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # first deploy: nothing published yet
        raise


def restore(site_url: str):
    """Download the published data into data/ so this run builds on the last one."""
    base = site_url.rstrip("/") + "/data/"
    news = fetch_json(base + "news.json")
    if not news:
        print("No published data yet: starting fresh.")
        return
    scraper.save(news)
    index = fetch_json(base + "editions/index.json") or []
    editions.EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    restored = 0
    for entry in index[: editions.BACKFILL_DAYS + 7]:
        day = entry["date"]
        raw = fetch_json(base + f"editions/raw/{day}.json")
        if raw:
            (editions.EDITIONS_DIR / f"{day}.json").write_text(json.dumps(raw, ensure_ascii=False))
            restored += 1
    print(f"Restored {len(news['posts'])} posts and {restored} daily editions from {site_url}")


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def build():
    data = scraper.scrape_all(scraper.load())
    scraper.save(data)
    editions.update(data)
    ok = sum(s["ok"] for s in data["sources"])
    print(f"Scraped {len(data['posts'])} posts, {ok}/{len(data['sources'])} sources ok")

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "data").mkdir(parents=True)

    # The page, with one line added so it reads static files instead of the local API.
    html = (ROOT / "static" / "index.html").read_text()
    html = html.replace("</head>", "<script>window.AIWIRE_STATIC = true;</script>\n</head>", 1)
    (SITE / "index.html").write_text(html)
    shutil.copytree(ROOT / "static" / "logos", SITE / "logos")  # company logos (tools/fetch_logos.py)

    write(SITE / "data" / "news.json", data)
    index = editions.index()
    write(SITE / "data" / "editions" / "index.json", index)
    raw_dir = SITE / "data" / "editions" / "raw"
    raw_dir.mkdir(parents=True)
    for entry in index:
        day = entry["date"]
        write(SITE / "data" / "editions" / f"{day}.json", editions.get(day))  # shaped for the page
        shutil.copy(editions.EDITIONS_DIR / f"{day}.json", raw_dir / f"{day}.json")  # for the next restore
    (SITE / ".nojekyll").write_text("")  # serve files as-is; skip GitHub's Jekyll processing
    size = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    print(f"Wrote site/ ({len(index)} daily editions, {size / 1e6:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) < 3:
            sys.exit("usage: python build.py restore <published site URL>")
        restore(sys.argv[2])
    else:
        build()
