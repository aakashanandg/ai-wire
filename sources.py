"""Where the posts come from. Add a source by adding one entry here.

AI Wire covers two things: system design, and AI system design (agents, RAG,
evals, LLM apps, inference). Every post is filtered through topics.is_focused,
so a source only needs to publish on-topic posts some of the time.

kind:
  rss   - an RSS/Atom feed (preferred: stable and cheap)
  html  - scrape a listing page for links matching `link_pattern`
  hn    - Hacker News stories, via the Algolia search API

group:
  lab          - AI labs' engineering and research blogs
  engineering  - company engineering blogs: how real systems are built and scaled
  learning     - newsletters and engineers who write about system design and AI engineering

focused (optional, default False):
  True when nearly every post is an on-topic technical write-up, so posts count
  as deep dives without needing a topic keyword in the title.
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
     "url": "https://huggingface.co/blog/feed.xml"},
    {"id": "microsoft-research", "name": "Microsoft Research", "org": "Microsoft", "group": "lab", "kind": "rss",
     "url": "https://www.microsoft.com/en-us/research/feed/"},

    # --- Engineering blogs: how big systems are designed and run ---------------
    {"id": "meta-eng", "name": "Engineering at Meta", "org": "Meta", "group": "engineering", "kind": "rss",
     "url": "https://engineering.fb.com/feed/", "focused": True},
    {"id": "netflix", "name": "Netflix TechBlog", "org": "Netflix", "group": "engineering", "kind": "rss",
     "url": "https://netflixtechblog.com/feed", "focused": True},
    {"id": "cloudflare", "name": "Cloudflare", "org": "Cloudflare", "group": "engineering", "kind": "rss",
     "url": "https://blog.cloudflare.com/rss/"},
    {"id": "github-eng", "name": "GitHub Engineering", "org": "GitHub", "group": "engineering", "kind": "rss",
     "url": "https://github.blog/engineering/feed/", "focused": True},
    {"id": "airbnb", "name": "Airbnb Engineering", "org": "Airbnb", "group": "engineering", "kind": "rss",
     "url": "https://medium.com/feed/airbnb-engineering", "focused": True},
    {"id": "dropbox", "name": "Dropbox Tech", "org": "Dropbox", "group": "engineering", "kind": "rss",
     "url": "https://dropbox.tech/feed", "focused": True},
    {"id": "slack", "name": "Slack Engineering", "org": "Slack", "group": "engineering", "kind": "rss",
     "url": "https://slack.engineering/feed/", "focused": True},
    {"id": "pinterest", "name": "Pinterest Engineering", "org": "Pinterest", "group": "engineering", "kind": "rss",
     "url": "https://medium.com/feed/pinterest-engineering", "focused": True},
    {"id": "shopify", "name": "Shopify Engineering", "org": "Shopify", "group": "engineering", "kind": "rss",
     "url": "https://shopify.engineering/blog.atom"},
    {"id": "spotify", "name": "Spotify Engineering", "org": "Spotify", "group": "engineering", "kind": "rss",
     "url": "https://engineering.atspotify.com/feed/", "focused": True},
    {"id": "aws-arch", "name": "AWS Architecture Blog", "org": "AWS", "group": "engineering", "kind": "rss",
     "url": "https://aws.amazon.com/blogs/architecture/feed/", "focused": True},
    {"id": "databricks", "name": "Databricks", "org": "Databricks", "group": "engineering", "kind": "rss",
     "url": "https://www.databricks.com/feed"},
    {"id": "langchain", "name": "LangChain", "org": "LangChain", "group": "engineering", "kind": "rss",
     "url": "https://www.langchain.com/blog/rss.xml"},
    {"id": "infoq-arch", "name": "InfoQ Architecture", "org": "InfoQ", "group": "engineering", "kind": "rss",
     "url": "https://feed.infoq.com/architecture-design/"},

    # --- Newsletters and engineers ------------------------------------------
    {"id": "bytebytego", "name": "ByteByteGo", "org": "ByteByteGo", "group": "learning", "kind": "rss",
     "url": "https://blog.bytebytego.com/feed", "focused": True},
    {"id": "systemdesign-one", "name": "The System Design Newsletter", "org": "System Design Newsletter",
     "group": "learning", "kind": "rss", "url": "https://newsletter.systemdesign.one/feed", "focused": True},
    {"id": "sd-codex", "name": "System Design Codex", "org": "System Design Codex", "group": "learning",
     "kind": "rss", "url": "https://newsletter.systemdesigncodex.com/feed", "focused": True},
    {"id": "arpit", "name": "Arpit Bhayani", "org": "Arpit Bhayani", "group": "learning", "kind": "rss",
     "url": "https://arpitbhayani.me/rss.xml", "focused": True},
    {"id": "vogels", "name": "All Things Distributed", "org": "Werner Vogels", "group": "learning", "kind": "rss",
     "url": "https://www.allthingsdistributed.com/atom.xml", "focused": True},
    {"id": "brooker", "name": "Marc Brooker", "org": "Marc Brooker", "group": "learning", "kind": "rss",
     "url": "https://brooker.co.za/blog/rss.xml", "focused": True},
    {"id": "murat", "name": "Murat Demirbas", "org": "Murat Demirbas", "group": "learning", "kind": "rss",
     "url": "https://muratbuffalo.blogspot.com/feeds/posts/default", "focused": True},
    {"id": "pragmatic", "name": "The Pragmatic Engineer", "org": "Pragmatic Engineer", "group": "learning", "kind": "rss",
     "url": "https://newsletter.pragmaticengineer.com/feed"},
    {"id": "fowler", "name": "Martin Fowler", "org": "Martin Fowler", "group": "learning", "kind": "rss",
     "url": "https://martinfowler.com/feed.atom"},
    {"id": "simonw", "name": "Simon Willison", "org": "Simon Willison", "group": "learning", "kind": "rss",
     "url": "https://simonwillison.net/atom/entries/", "focused": True},
    {"id": "hamel", "name": "Hamel Husain", "org": "Hamel Husain", "group": "learning", "kind": "rss",
     "url": "https://hamel.dev/index.xml", "focused": True},
    {"id": "latent-space", "name": "Latent Space", "org": "Latent Space", "group": "learning", "kind": "rss",
     "url": "https://www.latent.space/feed"},
    {"id": "eugeneyan", "name": "Eugene Yan", "org": "Eugene Yan", "group": "learning", "kind": "rss",
     "url": "https://eugeneyan.com/rss/", "focused": True},
    {"id": "lilianweng", "name": "Lilian Weng", "org": "Lilian Weng", "group": "learning", "kind": "rss",
     "url": "https://lilianweng.github.io/index.xml", "focused": True},

    # --- Community -----------------------------------------------------------
    {"id": "hn", "name": "Hacker News", "org": "Hacker News", "group": "community", "kind": "hn",
     "query": "agents LLM RAG MCP inference evals architecture distributed database scaling latency "
              "postgres kafka kubernetes caching outage postmortem",
     "min_points": 40, "days": 7},
]
