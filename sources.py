"""Where the posts come from. Add a source by adding one entry here.

AI Wire follows company engineering blogs, and keeps their posts on two
things: system design, and AI system design (agents, RAG, evals, LLM apps,
inference). Every post is filtered through topics.is_focused, so a blog only
needs to publish on-topic posts some of the time.

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
    # Company engineering blogs: how real systems are designed, built and run.
    {"id": "anthropic-eng", "name": "Anthropic Engineering", "org": "Anthropic", "group": "engineering", "kind": "html",
     "url": "https://www.anthropic.com/engineering", "link_pattern": r"^/engineering/[\w-]+$", "focused": True},
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
]
