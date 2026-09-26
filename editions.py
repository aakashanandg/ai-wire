"""Daily editions: one saved file per day, like a newsletter archive.

After every scrape, each post is filed under the day it was published (in this
computer's time zone) in data/editions/YYYY-MM-DD.json. Files are only ever
added to, so an edition stays complete even after its posts fall off the
source feeds (most feeds only list their latest 20-40 posts).
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

EDITIONS_DIR = Path(__file__).parent / "data" / "editions"
BACKFILL_DAYS = 60  # on first run, build editions for this many past days
HN_PER_EDITION = 10


def local_day(iso: str) -> str:
    return datetime.fromisoformat(iso).astimezone().date().isoformat()


def update(data: dict) -> int:
    """File the latest scrape into daily editions. Returns how many editions changed."""
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    oldest = (date.today() - timedelta(days=BACKFILL_DAYS)).isoformat()

    by_day: dict[str, list[dict]] = {}
    for p in data["posts"]:
        day = local_day(p["date"] or p["first_seen"])
        if day >= oldest:
            by_day.setdefault(day, []).append(p)

    changed = 0
    for day, posts in by_day.items():
        path = EDITIONS_DIR / f"{day}.json"
        edition = load(day) or {"date": day, "posts": []}
        merged = {p["url"]: p for p in edition["posts"]}
        for p in posts:
            merged[p["url"]] = {**merged.get(p["url"], {}), **p}  # refresh points/comments, keep the rest
        new_posts = sorted(merged.values(), key=lambda p: p["date"] or p["first_seen"], reverse=True)
        if new_posts != edition["posts"]:
            edition["posts"] = new_posts
            edition["updated"] = data["updated"]
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(edition, indent=1, ensure_ascii=False))
            tmp.replace(path)
            changed += 1
    return changed


def load(day: str) -> dict | None:
    try:
        date.fromisoformat(day)  # also stops path tricks like "../../etc"
        return json.loads((EDITIONS_DIR / f"{day}.json").read_text())
    except (ValueError, FileNotFoundError, json.JSONDecodeError):
        return None


def get(day: str) -> dict | None:
    """One edition, shaped for reading: lab posts grouped by company, top HN stories."""
    edition = load(day)
    if not edition:
        return None
    labs = [p for p in edition["posts"] if p["source"] != "hn"]
    hn = sorted((p for p in edition["posts"] if p["source"] == "hn"), key=lambda p: p.get("points", 0), reverse=True)
    groups: dict[str, list[dict]] = {}
    for p in labs:
        groups.setdefault(p["org"], []).append(p)
    return {
        "date": day,
        "updated": edition.get("updated"),
        "labs": [{"org": org, "posts": posts} for org, posts in sorted(groups.items(), key=lambda g: -len(g[1]))],
        "hn": hn[:HN_PER_EDITION],
        "counts": {"labs": len(labs), "orgs": len(groups), "hn": len(hn)},
    }


def week(end: str | None = None) -> dict:
    """Seven days ending on `end` (default today), newest first, with the week's biggest stories."""
    end_day = date.fromisoformat(end) if end else date.today()
    end_day = min(end_day, date.today())
    days = [(end_day - timedelta(days=i)).isoformat() for i in range(7)]
    editions = [get(d) or {"date": d, "labs": [], "hn": [], "counts": {"labs": 0, "orgs": 0, "hn": 0}} for d in days]

    # The week's top stories: every HN story of the week, ranked by points.
    top = sorted((p for e in editions for p in e["hn"]), key=lambda p: p.get("points", 0), reverse=True)[:5]
    oldest_saved = min((p.stem for p in EDITIONS_DIR.glob("*.json")), default=days[-1])
    return {
        "start": days[-1],
        "end": days[0],
        "days": editions,
        "top": top,
        "counts": {k: sum(e["counts"][k] for e in editions) for k in ("labs", "hn")},
        "older": (end_day - timedelta(days=7)).isoformat() if oldest_saved < days[-1] else None,
        "newer": (end_day + timedelta(days=7)).isoformat() if end_day < date.today() else None,
    }


def index() -> list[dict]:
    """Every edition, newest first, with post counts (for the archive list)."""
    out = []
    for path in sorted(EDITIONS_DIR.glob("*.json"), reverse=True):
        try:
            posts = json.loads(path.read_text())["posts"]
        except (json.JSONDecodeError, KeyError):
            continue
        labs = sum(p["source"] != "hn" for p in posts)
        out.append({"date": path.stem, "labs": labs, "hn": len(posts) - labs})
    return out
