"""Your reading progress: saved and read posts, stored in data/progress.json.

Each entry keeps a copy of the post, so your reading list survives after the
post drops off its source feed.
"""

import json
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

PROGRESS_FILE = Path(__file__).parent / "data" / "progress.json"
_lock = threading.Lock()
KEEP_FIELDS = ("title", "url", "date", "summary", "source", "source_name", "org", "group", "topics", "deep_dive")


def load() -> dict:
    try:
        return json.loads(PROGRESS_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"posts": {}}


def _save(data: dict):
    PROGRESS_FILE.parent.mkdir(exist_ok=True)
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    tmp.replace(PROGRESS_FILE)


def update(post: dict, saved: bool | None = None, read: bool | None = None) -> dict:
    """Set saved and/or read for one post. Passing None leaves that flag as it is."""
    if not str(post.get("url", "")).startswith(("http://", "https://")):
        raise ValueError("post.url must be an http(s) URL")
    now = datetime.now(timezone.utc).isoformat()
    with _lock:
        data = load()
        entry = data["posts"].get(post["url"], {})
        entry.update({k: post[k] for k in KEEP_FIELDS if k in post})
        if saved is not None:
            entry["saved_at"] = now if saved else None
        if read is not None:
            entry["read_at"] = now if read else None
        if entry.get("saved_at") or entry.get("read_at"):
            data["posts"][post["url"]] = entry
        else:
            data["posts"].pop(post["url"], None)  # nothing left to remember
        _save(data)
        return summary(data)


def summary(data: dict | None = None) -> dict:
    """Everything the page needs: the entries plus stats for the progress panel."""
    data = data or load()
    entries = list(data["posts"].values())
    read = [e for e in entries if e.get("read_at")]
    read_days = {datetime.fromisoformat(e["read_at"]).astimezone().date() for e in read}

    # Streak: consecutive days with at least one read, ending today (or yesterday,
    # so the streak doesn't look broken first thing in the morning).
    streak, day = 0, date.today()
    if day not in read_days:
        day -= timedelta(days=1)
    while day in read_days:
        streak += 1
        day -= timedelta(days=1)

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    by_topic: dict[str, int] = {}
    for e in read:
        for t in e.get("topics") or ["general"]:
            by_topic[t] = by_topic.get(t, 0) + 1
    return {
        "posts": data["posts"],
        "stats": {
            "read": len(read),
            "saved": sum(1 for e in entries if e.get("saved_at") and not e.get("read_at")),
            "read_this_week": sum(1 for e in read if datetime.fromisoformat(e["read_at"]) > week_ago),
            "streak": streak,
            "by_topic": by_topic,
        },
    }
