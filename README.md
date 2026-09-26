# AI Wire

The latest posts from AI lab blogs and AI stories on Hacker News, as a **daily edition** you can read like a newsletter, or as a **live feed**.

**Sources:** Anthropic (Engineering + News), OpenAI, Google DeepMind, Google Research, Meta AI, Mistral, Hugging Face, NVIDIA, Microsoft Research, Berkeley AI Research, Hacker News.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py            # open http://localhost:8000
```

Dates follow this computer's time zone. The server scrapes all sources at startup and then every 30 minutes (`--interval 15` to change). The page's **Refresh** button scrapes immediately. To scrape without the server, run `python scraper.py`.

## How it works

| File | Role |
|---|---|
| `sources.py` | The list of sources. Add one by adding an entry. |
| `scraper.py` | Fetches all sources in parallel, normalizes posts to `{title, url, date, summary, source}`, and writes `data/news.json`. |
| `editions.py` | Files each post under the day it was published and saves one edition per day in `data/editions/`. Editions are only added to, so old days stay complete after posts drop off the source feeds. |
| `server.py` | Serves the page and `/api/news`, and refreshes in the background. Python standard library only. |
| `static/index.html` | The page. **Daily edition** (default): one day at a time with top Hacker News stories then posts grouped by lab; use ← → or the date menu to move between days, and share a day with a link like `/#2026-09-22`. **Live feed**: everything newest first, with lab filters and search. Dark mode by default. |

Three kinds of source:

- **`rss`**: preferred. Stable and cheap.
- **`html`**: for sites without a feed (Anthropic, Meta AI). It finds links matching `link_pattern` on the listing page, then looks in the surrounding card for a title and date, instead of relying on CSS class names that change with every redesign. If a card has no date, it opens the article to find one.
- **`hn`**: the Hacker News Algolia API, filtered to AI keywords and a minimum score.

A source that fails (site down, layout changed) doesn't break the page. It shows as crossed out in the filters and is listed in the footer.

## Adding a source

```python
# RSS feed
{"id": "cohere", "name": "Cohere", "org": "Cohere", "kind": "rss", "url": "https://.../rss.xml"},

# No feed: scrape the listing page
{"id": "xai", "name": "xAI", "org": "xAI", "kind": "html",
 "url": "https://x.ai/news", "link_pattern": r"^/news/[\w-]+$"},
```

Run `python scraper.py` to check that it returns posts with dates.

## Being a good citizen

The scraper fetches each listing page once per refresh (every 30 minutes by default), identifies itself with a User-Agent, and only stores titles, links and short summaries. Keep the interval reasonable, and check a site's terms before adding it.
