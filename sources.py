"""Where the news comes from. Add a source by adding one entry here.

kind:
  rss   - an RSS/Atom feed (preferred: stable and cheap)
  html  - scrape a listing page for links matching `link_pattern`
  hn    - Hacker News stories about AI, via the Algolia search API
"""

SOURCES = [
    # --- AI labs -------------------------------------------------------------
    {"id": "anthropic-eng", "name": "Anthropic Engineering", "org": "Anthropic", "kind": "html",
     "url": "https://www.anthropic.com/engineering", "link_pattern": r"^/engineering/[\w-]+$"},
    {"id": "anthropic-news", "name": "Anthropic News", "org": "Anthropic", "kind": "html",
     "url": "https://www.anthropic.com/news", "link_pattern": r"^/news/[\w-]+$"},
    {"id": "openai", "name": "OpenAI", "org": "OpenAI", "kind": "rss",
     "url": "https://openai.com/news/rss.xml"},
    {"id": "deepmind", "name": "Google DeepMind", "org": "Google", "kind": "rss",
     "url": "https://deepmind.google/blog/rss.xml"},
    {"id": "google-research", "name": "Google Research", "org": "Google", "kind": "rss",
     "url": "https://research.google/blog/rss/"},
    {"id": "meta-ai", "name": "Meta AI", "org": "Meta", "kind": "html",
     "url": "https://ai.meta.com/blog/", "link_pattern": r"^https://ai\.meta\.com/blog/[\w-]+/?$"},
    {"id": "mistral", "name": "Mistral AI", "org": "Mistral", "kind": "rss",
     "url": "https://mistral.ai/news/rss"},
    {"id": "huggingface", "name": "Hugging Face", "org": "Hugging Face", "kind": "rss",
     "url": "https://huggingface.co/blog/feed.xml"},
    {"id": "nvidia", "name": "NVIDIA", "org": "NVIDIA", "kind": "rss",
     "url": "https://blogs.nvidia.com/feed/"},
    {"id": "microsoft-research", "name": "Microsoft Research", "org": "Microsoft", "kind": "rss",
     "url": "https://www.microsoft.com/en-us/research/feed/"},
    {"id": "bair", "name": "Berkeley AI Research", "org": "Berkeley", "kind": "rss",
     "url": "https://bair.berkeley.edu/blog/feed.xml"},

    # --- Community -----------------------------------------------------------
    {"id": "hn", "name": "Hacker News", "org": "Hacker News", "kind": "hn",
     "query": "AI LLM GPT OpenAI Anthropic Claude Gemini DeepMind Llama Mistral agents",
     "min_points": 40, "days": 7},
]
