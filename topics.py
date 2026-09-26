"""Decide what AI Wire is about: system design and AI system design.

Every post is tagged with the tracks it covers and marked as a deep dive or an
announcement. Only focused posts are kept (see is_focused): technical write-ups
about how systems are built, not launches, company news or model papers.

Plain keyword rules: fast, free, predictable, and easy to tune. Edit the word
lists to change what lands where.
"""

import re

# track id -> (label, keywords). Keywords match whole words, case-insensitively;
# a trailing * matches any ending ("scal*" matches scale, scaling, scalable).
TOPICS = {
    "system-design": ("System design", [
        # architecture and data
        "system design", "architecture", "architect*", "distributed", "database*", "postgres*", "mysql",
        "sql", "nosql", "storage", "cach*", "cdn", "queue*", "kafka", "stream processing", "event-driven",
        "pub/sub", "data pipeline*", "replicat*", "shard*", "partition*", "eventual consistency",
        "strong consistency", "consistency model*", "consensus", "raft",
        "paxos", "transaction*", "index*", "search index*", "schema*", "migrat*", "microservice*",
        "monolith", "api design", "graphql", "grpc", "idempoten*", "backend", "service mesh", "multi-region",
        # scale, reliability, performance
        # (No bare "scale", "reliable", "resilience", "monitoring" or "performance": they show
        # up in every kind of post, from climate research to marketing.)
        "scalab*", "scaling", "autoscal*", "latency", "throughput", "tail latency", "load balanc*",
        "rate limit*", "backpressure", "reliability", "availability", "failover", "fault toleran*",
        "outage*", "postmortem", "post-mortem", "incident*", "observab*", "distributed tracing", "slo*",
        "kubernetes", "k8s", "cluster*", "networking", "real-time", "concurrency", "redis", "dynamodb",
    ]),
    "ai": ("AI system design", [
        # agents and LLM applications
        "agent*", "agentic", "multi-agent", "tool use", "tool calling", "function calling", "mcp",
        "model context protocol", "harness*", "rag", "retrieval", "retrieval-augmented", "vector*",
        "embedding*", "context engineering", "context window", "prompt*", "eval*", "guardrail*",
        "sandbox*", "computer use", "browser use", "coding agent*", "claude code", "codex", "copilot",
        "langgraph", "structured output*", "llm*", "llmops", "ai engineering", "ai application*",
        "ai system*", "ai infrastructure", "orchestrat*",
        # serving and inference
        "inference", "serving", "model serving", "gpu*", "tpu*", "kv cache", "prompt caching",
        "quantiz*", "fine-tun*", "finetun*", "batching", "speculative decoding", "token*",
    ]),
}

# Words that usually mean "announcement" rather than "something to learn from".
ANNOUNCEMENT = re.compile(
    r"\b(introducing|announc\w*|partner\w*|customers?|case study|welcome|launch\w*|available now|now available|"
    r"joins?|hiring|funding|raises|pricing|event|webinar|conference|keynote|summit|award|expands?|"
    r"academy|program|remarks|policy|election|government|boosts? sales|saves?|widens?|access to|extends?|"
    r"helps?|meet|celebrat\w*|recap|roundup|this week|weekly|newsletter|podcast|interview|livestream|"
    r"enroll\w*|last call|fragments|the pulse|new in|what's new|release notes|changelog)\b"
    r"|^\[AINews\]",
    re.I,
)


# Customer stories and product updates. Checked only on mixed blogs (labs, vendor
# blogs): focused engineering blogs can say "cut latency 40%" and mean it.
MARKETING = re.compile(
    r"\bwith (codex|chatgpt|openai|gpt[\w.\u2011-]*|claude|gemini|langsmith|langgraph|deep agents|databricks)\b"
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
    r"^(?:How )?(?!We\b|I\b|To\b|Do\b|AI\b)[A-Z][\w&.'\u2019-]*(?: [A-Z][\w&.'\u2019-]*)* "
    r"(?:brings|automates|builds|uses|used|is redesigning|rebuilt|named|widens|cuts?)\b"
    r"|^How (?:engineers|teams|developers) at\b"
)

# News, politics and security incidents: common on Hacker News, not design lessons.
NEWS = re.compile(
    r"\b(court|judge|lawsuit|sues?|ftc|feds|government|congress|senate|regulat\w*|bans?|laws?|policy|"
    r"election|military|pentagon|nsa|hack(s|ed)?|layoffs?|stocks?|ipo|funding|acquir\w*|ceo|critics|"
    r"medicare|citizenship|immigration|drones?|criminal\w*|best llm|price war)\b",
    re.I,
)


def _compile(words: list[str]) -> re.Pattern:
    parts = [re.escape(w[:-1]) + r"\w*" if w.endswith("*") else re.escape(w) for w in words]
    return re.compile(r"\b(" + "|".join(parts) + r")\b", re.I)


PATTERNS = {tid: _compile(words) for tid, (_, words) in TOPICS.items()}
LABELS = {tid: label for tid, (label, _) in TOPICS.items()}


def classify(post: dict, source: dict) -> None:
    """Add `topics` (track ids, strongest first) and `deep_dive` (bool) to a post, in place."""
    text = f"{post['title']} {post.get('summary', '')} {' '.join(post.get('tags', []))}"
    # Titles count double: a keyword in the title says more than one in the summary.
    scores = {tid: 2 * len(p.findall(post["title"])) + len(p.findall(text)) for tid, p in PATTERNS.items()}
    post["topics"] = [tid for tid, s in sorted(scores.items(), key=lambda kv: -kv[1]) if s >= 2]

    if source["group"] == "community" and NEWS.search(post["title"]):
        post["topics"] = []  # news, not a design discussion
    if source["group"] == "community" or ANNOUNCEMENT.search(post["title"]):
        post["deep_dive"] = False
    elif not source.get("focused") and (MARKETING.search(post["title"]) or CUSTOMER.search(post["title"])):
        post["deep_dive"] = False
    elif source.get("focused"):
        post["deep_dive"] = True
    else:
        # Mixed blogs (labs, big company blogs) also post news and marketing:
        # require a track keyword in the title itself.
        post["deep_dive"] = any(PATTERNS[t].search(post["title"]) for t in post["topics"])


def is_focused(post: dict) -> bool:
    """Keep only system design and AI system design: deep dives, or HN stories on those topics."""
    if not post.get("topics"):
        return False
    return post.get("deep_dive", False) or post.get("group") == "community"
