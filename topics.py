"""Tag posts with learning topics, and tell deep dives apart from announcements.

Plain keyword rules: fast, free, predictable, and easy to tune. A post can have
several topics. Edit the word lists to change what lands where.
"""

import re

# topic id -> (label, keywords). Keywords match whole words, case-insensitively;
# a trailing * matches any ending ("scal*" matches scale, scaling, scalable).
TOPICS = {
    "agents": ("AI agents", [
        "agent*", "agentic", "tool use", "tool calling", "function calling", "mcp", "model context protocol",
        "harness*", "rag", "retrieval", "context engineering", "context window", "prompt*", "eval*",
        "coding assistant*", "claude code", "codex", "copilot", "langgraph", "orchestrat*", "workflow*",
        "memory", "guardrail*", "sandbox*", "computer use", "browser use", "autonomous",
    ]),
    "system-design": ("System design", [
        "scal*", "distributed", "architecture", "architect*", "database*", "cach*", "queue*", "kafka",
        "latency", "throughput", "replicat*", "shard*", "partition*", "consisten*", "microservice*",
        "storage", "migrat*", "reliab*", "outage*", "postmortem", "post-mortem", "incident*", "load balanc*",
        "rate limit*", "cdn", "observab*", "availability", "failover", "consensus", "event-driven",
        "stream processing", "data pipeline*", "api design", "graphql", "grpc", "idempoten*", "backend",
        "service mesh", "search index*", "real-time", "multi-region", "monolith",
    ]),
    "infra": ("Infra & performance", [
        "gpu*", "tpu*", "kubernetes", "k8s", "inference", "serving", "compute", "data center*", "datacenter*",
        "performance", "optimi*", "compiler*", "kernel*", "cuda", "memory bandwidth", "cluster*", "cloud",
        "networking", "rust", "wasm", "webassembly", "profil*", "benchmark*", "cost*", "efficien*",
    ]),
    "research": ("LLM research", [
        "training", "pretrain*", "fine-tun*", "finetun*", "reinforcement learning", "rlhf", "rl",
        "alignment", "interpretab*", "reasoning", "transformer*", "diffusion", "embedding*", "multimodal",
        "distillation", "quantiz*", "tokeniz*", "scaling law*", "paper", "dataset*", "model training",
        "world model*", "attention mechanism", "mixture of experts", "moe", "long context",
    ]),
}

# Words that usually mean "announcement" rather than "something to learn from".
ANNOUNCEMENT = re.compile(
    r"\b(introducing|announc\w*|partner\w*|customers?|case study|welcome|launch\w*|available now|now available|"
    r"joins?|hiring|funding|raises|pricing|event|webinar|conference|keynote|summit|award|expands?|"
    r"academy|program|remarks|policy|election|government|boosts? sales|saves?|widens?|access to|extends?|"
    r"helps?|meet|celebrat\w*|recap|roundup|this week|weekly|newsletter|podcast|interview|livestream|"
    r"enroll\w*|last call|fragments|the pulse)\b"
    r"|^\[AINews\]",
    re.I,
)


def _compile(words: list[str]) -> re.Pattern:
    parts = [re.escape(w[:-1]) + r"\w*" if w.endswith("*") else re.escape(w) for w in words]
    return re.compile(r"\b(" + "|".join(parts) + r")\b", re.I)


PATTERNS = {tid: _compile(words) for tid, (_, words) in TOPICS.items()}
LABELS = {tid: label for tid, (label, _) in TOPICS.items()}


def classify(post: dict, source: dict) -> None:
    """Add `topics` (list of topic ids) and `deep_dive` (bool) to a post, in place."""
    text = f"{post['title']} {post.get('summary', '')} {' '.join(post.get('tags', []))}"
    # Titles count double: a keyword in the title says more than one in the summary.
    scores = {tid: 2 * len(p.findall(post["title"])) + len(p.findall(text)) for tid, p in PATTERNS.items()}
    topics = [tid for tid, s in sorted(scores.items(), key=lambda kv: -kv[1]) if s >= 2]
    # "research" words like "model" are everywhere in AI news; only keep it as a
    # second topic when it is clearly the main subject.
    if "research" in topics and topics[0] != "research":
        topics.remove("research")
    post["topics"] = topics[:2]

    if source["group"] == "community" or ANNOUNCEMENT.search(post["title"]):
        post["deep_dive"] = False
    elif "deep_dive" in source:
        post["deep_dive"] = source["deep_dive"]
    elif source["group"] == "lab":
        # Lab blogs mix launches with technical posts: need a topic word in the title itself.
        post["deep_dive"] = any(PATTERNS[t].search(post["title"]) for t in topics)
    else:
        post["deep_dive"] = True
