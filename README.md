# AI Wire

The latest posts from AI lab blogs and AI stories on Hacker News, as a live **Feed** or a **This week** timeline.

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
| `editions.py` | Files each post under the day it was published (one file per day in `data/editions/`) and builds the week view. Files are only added to, so past weeks stay complete after posts drop off the source feeds. Hacker News history starts from your first run, because its search only looks back 7 days. |
| `server.py` | Serves the page and `/api/news`, and refreshes in the background. Python standard library only. |
| `static/index.html` | The page, dark mode by default. **Feed** (default): everything newest first, with lab filters, search and the latest Hacker News stories. **This week**: a 7-day strip showing how busy each day was, the week's biggest stories, then a day-by-day timeline of every lab post plus each day's top 3 Hacker News stories. Browse older weeks with ← →, or link to one like `/#week-2026-09-19`. |

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
