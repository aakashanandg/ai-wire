"""Decide what AI Wire keeps: AI news that's trending, and AI engineering deep dives.

  - Hacker News stories are kept when their title is about AI.
  - Blog posts are kept when they're technical write-ups about building with AI,
    not launches, customer stories or company news.

Plain keyword rules: fast, free, predictable, and easy to tune. Edit the word
lists to change what gets in.
"""

import re

# Keywords match whole words, case-insensitively; a trailing * matches any
# ending ("agent*" matches agent, agents, agentic).
GENERAL_AI_WORDS = [
    # the field
    "ai", "genai", "generative ai", "machine learning", "ml", "llm*", "language model*", "foundation model*",
    "neural", "deep learning", "transformer*", "multimodal",
    # models and labs (mostly for Hacker News titles)
    "gpt*", "chatgpt", "claude", "gemini", "llama", "mistral", "openai", "anthropic", "deepmind",
]
# How AI systems are built. AI labs mostly write about AI, so their titles must
# contain one of these to count as an engineering post (not just "AI" or a model name).
ENGINEERING_WORDS = [
    # building with AI
    "agent*", "agentic", "multi-agent", "tool use", "tool calling", "function calling", "mcp",
    "model context protocol", "harness*", "rag", "retrieval", "retrieval-augmented", "vector*",
    "embedding*", "context engineering", "context window", "prompt*", "eval*", "guardrail*",
    "computer use", "coding agent*", "claude code", "codex", "copilot", "langgraph", "structured output*",
    "llmops", "ai engineering", "fine-tun*", "finetun*", "rlhf", "reinforcement learning", "distillation",
    # serving and inference
    "inference", "model serving", "gpu*", "tpu*", "kv cache", "prompt caching", "quantiz*",
    "speculative decoding", "token*", "serving", "llm serving",
]
AI_WORDS = GENERAL_AI_WORDS + ENGINEERING_WORDS

# Launches, events and roundups: dropped from every blog.
ANNOUNCEMENT = re.compile(
    r"\b(introducing|announc\w*|partner\w*|customers?|case study|welcome|launch\w*|available now|now available|"
    r"joins?|hiring|funding|raises|pricing|event|webinar|conference|keynote|summit|award|expands?|"
    r"academy|program|remarks|policy|election|government|boosts? sales|saves?|widens?|access to|extends?|"
    r"helps?|meet|celebrat\w*|recap|roundup|this week|weekly|newsletter|podcast|interview|livestream|"
    r"enroll\w*|last call|fragments|the pulse|new in|what's new|release notes|changelog)\b"
    r"|^\[AINews\]",
    re.I,
)

# Customer stories and product updates: dropped from mixed blogs (labs, vendors,
# company blogs). AI-focused blogs can say "cut latency 40%" and mean it.
MARKETING = re.compile(
    r"\bwith (codex|chatgpt|openai|gpt[\w.‑-]*|claude|gemini|langsmith|langgraph|deep agents|databricks)\b"
    r"|\b\d+(\.\d+)?\s?%|\bproductivity\b|\blessons from\b|\buse cases\b|\bnow in\b|\bnow supports\b"
    r"|\bdelivers\b|\blangsmith\b|\bmanaged deep agents\b|\bhow (a|an|one) \w+ (uses|use)\b"
    r"|\b(enterprises?|employees|leader|gartner|investments?|community|letter|governor|brings|comes? to|named|"
    r"unlocks|transforming|for every|everything|generally available|roi|retention|is now the|age of|era|"
    r"unveil\w*|trusted ai|responsible ai|playbook|workspace)\b",
    re.I,
)
# Company-as-subject headlines: "Polimill builds…", "How Endava is redesigning…",
# "How engineers at Nextdoor use…". Case-sensitive; "How we built…" is kept.
CUSTOMER = re.compile(
    r"^(?:How )?(?!We\b|I\b|To\b|Do\b|AI\b)[A-Z][\w&.'’-]*(?: [A-Z][\w&.'’-]*)* "
    r"(?:brings|automates|builds|uses|used|is redesigning|rebuilt|named|widens|cuts?)\b"
    r"|^How (?:engineers|teams|developers) at\b"
)


def _compile(words: list[str]) -> re.Pattern:
    parts = [re.escape(w[:-1]) + r"\w*" if w.endswith("*") else re.escape(w) for w in words]
    return re.compile(r"\b(" + "|".join(parts) + r")\b", re.I)


AI = _compile(AI_WORDS)
ENGINEERING = _compile(ENGINEERING_WORDS)


def classify(post: dict, source: dict) -> None:
    """Add `topics` (["ai"] or []) and `deep_dive` (bool) to a post, in place."""
    title = post["title"]
    text = f"{title} {post.get('summary', '')} {' '.join(post.get('tags', []))}"
    # A keyword in the title counts double: one there, or two in the summary, is enough.
    score = 2 * len(AI.findall(title)) + len(AI.findall(text))
    post["topics"] = ["ai"] if score >= 2 else []

    if source["group"] == "community" or ANNOUNCEMENT.search(title):
        post["deep_dive"] = False
    elif source.get("focused"):
        post["deep_dive"] = True
    else:
        # Mixed blogs: the title itself must be about AI (for AI labs: about AI
        # engineering), and not read like marketing.
        on_topic = ENGINEERING if source["group"] == "lab" else AI
        post["deep_dive"] = bool(on_topic.search(title)) and not (MARKETING.search(title) or CUSTOMER.search(title))


def is_focused(post: dict) -> bool:
    """Trending news: any AI story on Hacker News. Blogs: AI deep dives only."""
    if not post.get("topics"):
        return False
    return post.get("group") == "community" or post.get("deep_dive", False)
