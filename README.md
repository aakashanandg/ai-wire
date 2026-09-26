# AI Wire

One page of **system design** and **AI system design** deep dives from company engineering blogs. It keeps only technical write-ups (no launches, customer stories or company news), sorts them into two sections, and updates every 30 minutes.

**Live:** https://aakashanandg.github.io/ai-wire/

**The page:** cards in two sections, *System design* and *AI system design*, newest first. Filter by blog, search, and switch between dark and light. At most 12 posts per blog, so no single company dominates.

**Blogs (15):** Anthropic Engineering, Engineering at Meta, Netflix TechBlog, Cloudflare, GitHub Engineering, Airbnb Engineering, Dropbox Tech, Slack Engineering, Pinterest Engineering, Shopify Engineering, Spotify Engineering, AWS Architecture Blog, Databricks, LangChain, InfoQ Architecture.

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
| `topics.py` | Tags each post with its track (system design / AI system design), decides whether it's a deep dive, and filters out announcements, customer stories and news. Only on-topic deep dives are kept. |
| `progress.py` | Reading-progress API used by earlier versions of the page (bookmarks, read marks); not used by the current page. |
| `editions.py` | Files each post under the day it was published (one file per day in `data/editions/`), a growing archive that earlier versions showed as a week timeline. Files are only added to, so past weeks stay complete after posts drop off the source feeds. Hacker News history starts from your first run, because its search only looks back 7 days. |
| `build.py` | Builds the static site for GitHub Pages (`site/`), and restores the previous run's data from the live site. |
| `server.py` | Serves the page and `/api/news`, and refreshes in the background. Python standard library only. |
| `static/index.html` | The page: one file, plain JavaScript. Colors follow [The Daily Diff](https://tdd.cat/) (dark by default, light available); fonts are Source Serif 4 and DM Sans. |

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

Sources marked `"focused": True` in `sources.py` publish almost nothing but deep dives, so their posts only need to match a track. Run `python scraper.py` to re-tag everything; the daily archive is re-checked against the rules on every update.

## Adding a source

```python
# RSS feed
{"id": "uber", "name": "Uber Engineering", "org": "Uber", "group": "engineering", "kind": "rss", "url": "https://.../rss.xml"},

# No feed: scrape the listing page
{"id": "xai", "name": "xAI Engineering", "org": "xAI", "group": "engineering", "kind": "html",
 "url": "https://x.ai/news", "link_pattern": r"^/news/[\w-]+$"},
```

Run `python scraper.py` to check that it returns posts with dates.

## Being a good citizen

The scraper fetches each listing page once per refresh (every 30 minutes by default), identifies itself with a User-Agent, and only stores titles, links and short summaries. Keep the interval reasonable, and check a site's terms before adding it.
