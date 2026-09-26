"""Where the posts come from. Add a source by adding one entry here.

AI Wire has two sections:
  - Trending AI news: the week's most-upvoted AI stories on Hacker News
  - AI engineering blogs: technical write-ups on building with AI (agents, RAG,
    evals, LLM apps, inference), filtered through topics.is_focused

kind:
  rss   - an RSS/Atom feed (preferred: stable and cheap)
  html  - scrape a listing page for links matching `link_pattern`
  hn    - Hacker News stories, via the Algolia search API

group:
  lab          - AI labs' engineering and research blogs
  engineering  - company engineering blogs (only their AI posts are kept)
  learning     - engineers who write about building with AI
  community    - Hacker News (the "Trending AI news" section)

max_posts (optional): overrides the per-source cap (scraper.MAX_PER_SOURCE).

focused (optional, default False):
  True for blogs that write almost only about AI engineering: their posts are
  kept whenever they're about AI. Other blogs need an AI keyword in the title.
"""

SOURCES = [
    # --- AI labs -------------------------------------------------------------
    {"id": "anthropic-eng", "name": "Anthropic Engineering", "org": "Anthropic", "group": "lab", "kind": "html",
     "url": "https://www.anthropic.com/engineering", "link_pattern": r"^/engineering/[\w-]+$", "focused": True},
    {"id": "openai", "name": "OpenAI", "org": "OpenAI", "group": "lab", "kind": "rss",
     "url": "https://openai.com/news/rss.xml"},
    {"id": "deepmind", "name": "Google DeepMind", "org": "Google", "group": "lab", "kind": "rss",
     "url": "https://deepmind.google/blog/rss.xml"},
    {"id": "google-research", "name": "Google Research", "org": "Google", "group": "lab", "kind": "rss",
     "url": "https://research.google/blog/rss/"},
    {"id": "huggingface", "name": "Hugging Face", "org": "Hugging Face", "group": "lab", "kind": "rss",
     "url": "https://huggingface.co/blog/feed.xml", "focused": True},
    {"id": "microsoft-research", "name": "Microsoft Research", "org": "Microsoft", "group": "lab", "kind": "rss",
     "url": "https://www.microsoft.com/en-us/research/feed/"},

    # --- Company engineering blogs (AI posts only) ---------------------------
    {"id": "meta-eng", "name": "Engineering at Meta", "org": "Meta", "group": "engineering", "kind": "rss",
     "url": "https://engineering.fb.com/feed/"},
    {"id": "netflix", "name": "Netflix TechBlog", "org": "Netflix", "group": "engineering", "kind": "rss",
     "url": "https://netflixtechblog.com/feed"},
    {"id": "cloudflare", "name": "Cloudflare", "org": "Cloudflare", "group": "engineering", "kind": "rss",
     "url": "https://blog.cloudflare.com/rss/"},
    {"id": "github-eng", "name": "GitHub Engineering", "org": "GitHub", "group": "engineering", "kind": "rss",
     "url": "https://github.blog/engineering/feed/"},
    {"id": "airbnb", "name": "Airbnb Engineering", "org": "Airbnb", "group": "engineering", "kind": "rss",
     "url": "https://medium.com/feed/airbnb-engineering"},
    {"id": "dropbox", "name": "Dropbox Tech", "org": "Dropbox", "group": "engineering", "kind": "rss",
     "url": "https://dropbox.tech/feed"},
    {"id": "slack", "name": "Slack Engineering", "org": "Slack", "group": "engineering", "kind": "rss",
     "url": "https://slack.engineering/feed/"},
    {"id": "pinterest", "name": "Pinterest Engineering", "org": "Pinterest", "group": "engineering", "kind": "rss",
     "url": "https://medium.com/feed/pinterest-engineering"},
    {"id": "shopify", "name": "Shopify Engineering", "org": "Shopify", "group": "engineering", "kind": "rss",
     "url": "https://shopify.engineering/blog.atom"},
    {"id": "spotify", "name": "Spotify Engineering", "org": "Spotify", "group": "engineering", "kind": "rss",
     "url": "https://engineering.atspotify.com/feed/"},
    {"id": "aws-arch", "name": "AWS Architecture Blog", "org": "AWS", "group": "engineering", "kind": "rss",
     "url": "https://aws.amazon.com/blogs/architecture/feed/"},
    {"id": "databricks", "name": "Databricks", "org": "Databricks", "group": "engineering", "kind": "rss",
     "url": "https://www.databricks.com/feed"},
    {"id": "langchain", "name": "LangChain", "org": "LangChain", "group": "engineering", "kind": "rss",
     "url": "https://www.langchain.com/blog/rss.xml"},

    # --- Engineers writing about building with AI ----------------------------
    {"id": "simonw", "name": "Simon Willison", "org": "Simon Willison", "group": "learning", "kind": "rss",
     "url": "https://simonwillison.net/atom/entries/", "focused": True},
    {"id": "hamel", "name": "Hamel Husain", "org": "Hamel Husain", "group": "learning", "kind": "rss",
     "url": "https://hamel.dev/index.xml", "focused": True},
    {"id": "eugeneyan", "name": "Eugene Yan", "org": "Eugene Yan", "group": "learning", "kind": "rss",
     "url": "https://eugeneyan.com/rss/", "focused": True},
    {"id": "lilianweng", "name": "Lilian Weng", "org": "Lilian Weng", "group": "learning", "kind": "rss",
     "url": "https://lilianweng.github.io/index.xml", "focused": True},
    {"id": "latent-space", "name": "Latent Space", "org": "Latent Space", "group": "learning", "kind": "rss",
     "url": "https://www.latent.space/feed", "focused": True},

    # --- Trending AI news ----------------------------------------------------
    {"id": "hn", "name": "Hacker News", "org": "Hacker News", "group": "community", "kind": "hn",
     "query": "AI LLM GPT OpenAI Anthropic Claude Gemini DeepMind Llama Mistral agents",
     "min_points": 40, "days": 7, "max_posts": 40},
]
