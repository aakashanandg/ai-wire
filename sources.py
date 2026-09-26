"""Where the news comes from. Add a source by adding one entry here.

kind:
  rss   - an RSS/Atom feed (preferred: stable and cheap)
  html  - scrape a listing page for links matching `link_pattern`
  hn    - Hacker News stories about AI, via the Algolia search API

group:
  lab          - AI labs: model launches, research, and their engineering blogs
  engineering  - company engineering blogs: how real systems are built and scaled
  learning     - newsletters and researchers who explain AI engineering and system design

deep_dive (optional, default True for engineering/learning, False for labs):
  whether posts are usually technical write-ups rather than announcements.
  Lab posts are classified one by one (see scraper.classify).
"""

SOURCES = [
    # --- AI labs -------------------------------------------------------------
    {"id": "anthropic-eng", "name": "Anthropic Engineering", "org": "Anthropic", "group": "lab", "kind": "html",
     "url": "https://www.anthropic.com/engineering", "link_pattern": r"^/engineering/[\w-]+$", "deep_dive": True},
    {"id": "anthropic-news", "name": "Anthropic News", "org": "Anthropic", "group": "lab", "kind": "html",
     "url": "https://www.anthropic.com/news", "link_pattern": r"^/news/[\w-]+$"},
    {"id": "openai", "name": "OpenAI", "org": "OpenAI", "group": "lab", "kind": "rss",
     "url": "https://openai.com/news/rss.xml"},
    {"id": "deepmind", "name": "Google DeepMind", "org": "Google", "group": "lab", "kind": "rss",
     "url": "https://deepmind.google/blog/rss.xml"},
    {"id": "google-research", "name": "Google Research", "org": "Google", "group": "lab", "kind": "rss",
     "url": "https://research.google/blog/rss/", "deep_dive": True},
    {"id": "meta-ai", "name": "Meta AI", "org": "Meta", "group": "lab", "kind": "html",
     "url": "https://ai.meta.com/blog/", "link_pattern": r"^https://ai\.meta\.com/blog/[\w-]+/?$"},
    {"id": "mistral", "name": "Mistral AI", "org": "Mistral", "group": "lab", "kind": "rss",
     "url": "https://mistral.ai/news/rss"},
    {"id": "huggingface", "name": "Hugging Face", "org": "Hugging Face", "group": "lab", "kind": "rss",
     "url": "https://huggingface.co/blog/feed.xml", "deep_dive": True},
    {"id": "nvidia", "name": "NVIDIA", "org": "NVIDIA", "group": "lab", "kind": "rss",
     "url": "https://blogs.nvidia.com/feed/"},
    {"id": "microsoft-research", "name": "Microsoft Research", "org": "Microsoft", "group": "lab", "kind": "rss",
     "url": "https://www.microsoft.com/en-us/research/feed/", "deep_dive": True},
    {"id": "bair", "name": "Berkeley AI Research", "org": "Berkeley", "group": "lab", "kind": "rss",
     "url": "https://bair.berkeley.edu/blog/feed.xml", "deep_dive": True},

    # --- Engineering blogs: how big systems are designed and run ---------------
    {"id": "meta-eng", "name": "Engineering at Meta", "org": "Meta", "group": "engineering", "kind": "rss",
     "url": "https://engineering.fb.com/feed/"},
    {"id": "netflix", "name": "Netflix TechBlog", "org": "Netflix", "group": "engineering", "kind": "rss",
     "url": "https://netflixtechblog.com/feed"},
    {"id": "cloudflare", "name": "Cloudflare", "org": "Cloudflare", "group": "engineering", "kind": "rss",
     "url": "https://blog.cloudflare.com/rss/"},
    {"id": "stripe", "name": "Stripe", "org": "Stripe", "group": "engineering", "kind": "rss",
     "url": "https://stripe.com/blog/feed.rss"},
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

    # --- Newsletters and researchers ----------------------------------------
    {"id": "bytebytego", "name": "ByteByteGo", "org": "ByteByteGo", "group": "learning", "kind": "rss",
     "url": "https://blog.bytebytego.com/feed"},
    {"id": "pragmatic", "name": "The Pragmatic Engineer", "org": "Pragmatic Engineer", "group": "learning", "kind": "rss",
     "url": "https://newsletter.pragmaticengineer.com/feed"},
    {"id": "fowler", "name": "Martin Fowler", "org": "Martin Fowler", "group": "learning", "kind": "rss",
     "url": "https://martinfowler.com/feed.atom"},
    {"id": "simonw", "name": "Simon Willison", "org": "Simon Willison", "group": "learning", "kind": "rss",
     "url": "https://simonwillison.net/atom/entries/"},
    {"id": "latent-space", "name": "Latent Space", "org": "Latent Space", "group": "learning", "kind": "rss",
     "url": "https://www.latent.space/feed"},
    {"id": "eugeneyan", "name": "Eugene Yan", "org": "Eugene Yan", "group": "learning", "kind": "rss",
     "url": "https://eugeneyan.com/rss/"},
    {"id": "lilianweng", "name": "Lilian Weng", "org": "Lilian Weng", "group": "learning", "kind": "rss",
     "url": "https://lilianweng.github.io/index.xml"},

    # --- Community -----------------------------------------------------------
    {"id": "hn", "name": "Hacker News", "org": "Hacker News", "group": "community", "kind": "hn",
     "query": "AI LLM GPT OpenAI Anthropic Claude Gemini DeepMind Llama Mistral agents",
     "min_points": 40, "days": 7},
]
