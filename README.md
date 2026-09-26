# AI Wire

A reading desk for software engineers who want to get better at **system design** and **AI system design**. It collects deep dives from AI labs, company engineering blogs and engineers who write about building at scale, keeps only the technical write-ups (no launches, company news or model papers), and tracks what you've read.

**Live:** https://aakashanandg.github.io/ai-wire/

**Views**
- **Feed**: cards in two sections, *System design* and *AI system design* (or a date-ordered list). Filter by *AI labs*, *Engineering blogs* or *Newsletters & engineers*, then by source. On the side: Hacker News stories about system design and AI engineering.
- **This week**: a 7-day strip, the week's most-discussed Hacker News stories, and a day-by-day timeline. Browse older weeks with ← →.
- **Learn**: both tracks as a reading list. Bookmark posts, tick them off as read, and follow your streak and per-track progress.

**Sources (35)**
- *AI labs:* Anthropic Engineering, OpenAI, Google DeepMind, Google Research, Hugging Face, Microsoft Research
- *Engineering blogs:* Meta, Netflix, Cloudflare, GitHub, Airbnb, Dropbox, Slack, Pinterest, Shopify, Spotify, AWS Architecture, Databricks, LangChain, InfoQ Architecture
- *Newsletters & engineers:* ByteByteGo, The System Design Newsletter, System Design Codex, Arpit Bhayani, All Things Distributed (Werner Vogels), Marc Brooker, Murat Demirbas, The Pragmatic Engineer, Martin Fowler, Simon Willison, Hamel Husain, Latent Space, Eugene Yan, Lilian Weng
- *Community:* Hacker News

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py            # open http://localhost:8000
```

Dates follow this computer's time zone. The server scrapes all sources at startup and then every 30 minutes (`--interval 15` to change). The page's **Refresh** button scrapes immediately. To scrape without the server, run `python scraper.py`.

## Deploy to GitHub Pages (free)

`.github/workflows/update.yml` rebuilds the site every 30 minutes on GitHub's machines:

1. `python build.py restore <site URL>` downloads the currently published posts and daily archive, so history carries over between runs.
2. `python build.py` scrapes every source and writes a static copy of the site to `site/`.
3. GitHub Pages publishes `site/` at `https://<user>.github.io/<repo>/`.

On the static site, reading progress is stored in each visitor's browser. Use **Export progress / Import** in the Learn tab to move it between browsers. To set it up: push the repo, then Settings → Pages → Source: **GitHub Actions**, and run the workflow once from the Actions tab.

To try the static build locally: `python build.py && python -m http.server -d site 8001`.

## How it works

| File | Role |
|---|---|
| `sources.py` | The list of sources. Add one by adding an entry. |
| `scraper.py` | Fetches all sources in parallel, normalizes posts to `{title, url, date, summary, source}`, and writes `data/news.json`. |
| `topics.py` | Tags each post with its track (system design / AI system design), decides whether it's a deep dive, and filters out announcements, customer stories and news. Only on-topic deep dives are kept. |
| `progress.py` | Your saved and read posts plus stats (streak, per-topic counts), stored in `data/progress.json`. Each entry keeps a copy of the post, so your reading list survives after posts drop off their feeds. |
| `editions.py` | Files each post under the day it was published (one file per day in `data/editions/`) and builds the week view. Files are only added to, so past weeks stay complete after posts drop off the source feeds. Hacker News history starts from your first run, because its search only looks back 7 days. |
| `build.py` | Builds the static site for GitHub Pages (`site/`), and restores the previous run's data from the live site. |
| `server.py` | Serves the page and `/api/news`, and refreshes in the background. Python standard library only. |
| `static/index.html` | The page. Colors follow [The Daily Diff](https://tdd.cat/) (dark by default, light available); fonts are Source Serif 4 and DM Sans. Links: `/#week`, `/#week-2026-09-19`, `/#learn`. |

Three kinds of source:

- **`rss`**: preferred. Stable and cheap.
- **`html`**: for sites without a feed (Anthropic, Meta AI). It finds links matching `link_pattern` on the listing page, then looks in the surrounding card for a title and date, instead of relying on CSS class names that change with every redesign. If a card has no date, it opens the article to find one.
- **`hn`**: the Hacker News Algolia API, filtered to AI keywords and a minimum score.

A source that fails (site down, layout changed) doesn't break the page: its previous posts are kept, it shows crossed out in the filters, and it's listed in the footer.

## Tuning what gets in

Everything is keyword rules in `topics.py`:
- **`TOPICS`**: the words that put a post in *System design* or *AI system design*. A post needs one in its title, or two in its summary.
- **`ANNOUNCEMENT`**: launches, events and roundups, dropped from every source.
- **`MARKETING`** and **`CUSTOMER`**: customer stories and product updates ("X boosts productivity 30% with Y"), dropped from mixed blogs such as the AI labs.
- **`NEWS`**: politics, lawsuits and security incidents, dropped from Hacker News.

Sources marked `"focused": True` in `sources.py` publish almost nothing but deep dives, so their posts only need to match a track. Run `python scraper.py` to re-tag everything; the daily archive is re-checked against the rules on every update.

## Adding a source

```python
# RSS feed
{"id": "cohere", "name": "Cohere", "org": "Cohere", "group": "lab", "kind": "rss", "url": "https://.../rss.xml"},

# No feed: scrape the listing page
{"id": "xai", "name": "xAI", "org": "xAI", "group": "lab", "kind": "html",
 "url": "https://x.ai/news", "link_pattern": r"^/news/[\w-]+$"},
```

Run `python scraper.py` to check that it returns posts with dates.

## Being a good citizen

The scraper fetches each listing page once per refresh (every 30 minutes by default), identifies itself with a User-Agent, and only stores titles, links and short summaries. Keep the interval reasonable, and check a site's terms before adding it.
