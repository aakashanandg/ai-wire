"""Download a logo for every company in sources.py into static/logos/.

    python tools/fetch_logos.py            # fetch any missing logos
    python tools/fetch_logos.py --force    # re-download all of them

Logos are stored in the repo (not hot-linked), so the site never makes
visitors' browsers contact a third party. Run this after adding a source.
Uses Google's public favicon service, which returns a consistent PNG.
"""

import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sources import SOURCES  # noqa: E402

LOGOS = Path(__file__).resolve().parent.parent / "static" / "logos"

# Company -> website whose icon to use.
DOMAINS = {
    "Anthropic": "anthropic.com", "OpenAI": "openai.com", "Google": "google.com",
    "Hugging Face": "huggingface.co", "Microsoft": "microsoft.com", "Meta": "meta.com",
    "Netflix": "netflix.com", "Cloudflare": "cloudflare.com", "GitHub": "github.com",
    "Airbnb": "airbnb.com", "Dropbox": "dropbox.com", "Slack": "slack.com",
    "Pinterest": "pinterest.com", "Shopify": "shopify.com", "Spotify": "spotify.com",
    "AWS": "aws.amazon.com", "Databricks": "databricks.com", "LangChain": "langchain.com",
    "Simon Willison": "simonwillison.net", "Hamel Husain": "hamel.dev", "Eugene Yan": "eugeneyan.com",
    "Lilian Weng": "lilianweng.github.io", "Latent Space": "latent.space",
    "Hacker News": "news.ycombinator.com",
}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main(force: bool = False):
    LOGOS.mkdir(parents=True, exist_ok=True)
    for org in sorted({s["org"] for s in SOURCES}):
        path = LOGOS / f"{slug(org)}.png"
        if path.exists() and not force:
            continue
        domain = DOMAINS.get(org)
        if not domain:
            print(f"  no domain for {org!r}: add it to DOMAINS")
            continue
        url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Wire/1.0)"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            path.write_bytes(resp.read())
        print(f"  {org:<16} {path.stat().st_size:>6} bytes  {path.name}")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
