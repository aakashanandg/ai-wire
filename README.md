# AI Wire

What's trending in AI, and how teams are building with it. Two tabs, updated every 30 minutes:

- **AI news**: the week's most-upvoted AI stories on Hacker News, ranked by points.
- **AI engineering blogs**: technical write-ups on building with AI (agents, RAG, evals, LLM apps, inference) in a magazine layout, with company logos and a filter per company. Launches, customer stories and company news are filtered out.

**Live:** https://aakashanandg.github.io/ai-wire/

**Sources (25)**
- *AI labs:* Anthropic Engineering, OpenAI, Google DeepMind, Google Research, Hugging Face, Microsoft Research
- *Company engineering blogs (AI posts only):* Meta, Netflix, Cloudflare, GitHub, Airbnb, Dropbox, Slack, Pinterest, Shopify, Spotify, AWS Architecture, Databricks, LangChain
- *Engineers:* Simon Willison, Hamel Husain, Eugene Yan, Lilian Weng, Latent Space
- *Trending:* Hacker News

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

To set it up: push the repo, then Settings → Pages → Source: **GitHub Actions**, and run the workflow once from the Actions tab.

To try the static build locally: `python build.py && python -m http.server -d site 8001`.

## How it works

| File | Role |
|---|---|
| `sources.py` | The list of sources. Add one by adding an entry. |
| `scraper.py` | Fetches all sources in parallel, normalizes posts to `{title, url, date, summary, source}`, and writes `data/news.json`. |
| `topics.py` | Decides what's kept: AI stories from Hacker News, and AI engineering deep dives from the blogs (no announcements, customer stories or company news). |
| `progress.py` | Reading-progress API used by earlier versions of the page (bookmarks, read marks); not used by the current page. |
| `editions.py` | Files each post under the day it was published (one file per day in `data/editions/`), a growing archive that earlier versions showed as a week timeline. Files are only added to, so past weeks stay complete after posts drop off the source feeds. Hacker News history starts from your first run, because its search only looks back 7 days. |
| `build.py` | Builds the static site for GitHub Pages (`site/`), and restores the previous run's data from the live site. |
| `server.py` | Serves the page and `/api/news`, and refreshes in the background. Python standard library only. |
| `static/logos/` | Company logos, stored in the repo so visitors' browsers never contact a third party. Fetch new ones with `python tools/fetch_logos.py`. |
| `static/index.html` | The page: one file, plain JavaScript. Two tabs (`#news`, `#blogs`). Colors match Claude's light and dark themes (light by default). Claude's own fonts (Anthropic Serif and Sans) aren't licensed for other sites, so it uses the closest free ones: Source Serif 4 and Inter. |

Three kinds of source:

- **`rss`**: preferred. Stable and cheap.
- **`html`**: for sites without a feed (Anthropic, Meta AI). It finds links matching `link_pattern` on the listing page, then looks in the surrounding card for a title and date, instead of relying on CSS class names that change with every redesign. If a card has no date, it opens the article to find one.
- **`hn`**: the Hacker News Algolia API, filtered to AI keywords and a minimum score.

A source that fails (site down, layout changed) doesn't break the page: its previous posts are kept, it shows crossed out in the filters, and it's listed in the footer.

## Tuning what gets in

Everything is keyword rules in `topics.py`:
- **`AI_WORDS`**: a post must mention one of these (in the title, or twice in the summary). AI lab posts need one of the **`ENGINEERING_WORDS`** in the title, so "Reimagining advertising with AI" stays out.
- **`ANNOUNCEMENT`**: launches, events and roundups, dropped from every blog.
- **`MARKETING`** and **`CUSTOMER`**: customer stories and product updates, dropped from mixed blogs (labs, vendors, company blogs).

Blogs marked `"focused": True` in `sources.py` write almost only about AI engineering, so any AI post of theirs is kept. Each blog is capped at 12 posts (`MAX_PER_SOURCE` in `scraper.py`). Run `python scraper.py` to re-tag everything.

## Adding a source

```python
# RSS feed
{"id": "uber", "name": "Uber Engineering", "org": "Uber", "group": "engineering", "kind": "rss", "url": "https://.../rss.xml"},

# No feed: scrape the listing page
{"id": "xai", "name": "xAI Engineering", "org": "xAI", "group": "engineering", "kind": "html",
 "url": "https://x.ai/news", "link_pattern": r"^/news/[\w-]+$"},
```

Run `python scraper.py` to check that it returns posts with dates, and `python tools/fetch_logos.py` to download the new company's logo (add its website to `DOMAINS` first).

## Being a good citizen

The scraper fetches each listing page once per refresh (every 30 minutes by default), identifies itself with a User-Agent, and only stores titles, links and short summaries. Keep the interval reasonable, and check a site's terms before adding it.
