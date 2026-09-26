"""Serve the news page and keep the data fresh.

    python server.py            # http://localhost:8000
    python server.py --port 9000 --interval 15

Endpoints:
    GET  /              the page
    GET  /api/news      all posts + source status (JSON)
    POST /api/refresh   scrape now (returns when done)
"""

import argparse
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import scraper

STATIC = Path(__file__).parent / "static"
lock = threading.Lock()


def refresh():
    # Only one scrape at a time; a second caller just waits for the running one.
    with lock:
        data = scraper.scrape_all(scraper.load())
        scraper.save(data)
        ok = sum(s["ok"] for s in data["sources"])
        print(f"[{time.strftime('%H:%M:%S')}] refreshed: {len(data['posts'])} posts, {ok}/{len(data['sources'])} sources ok")


def refresh_forever(minutes: int):
    while True:
        try:
            refresh()
        except Exception as e:
            print(f"refresh failed: {e}")
        time.sleep(minutes * 60)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/news":
            return self.send_json(scraper.load() or {"updated": None, "sources": [], "posts": []})
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/refresh":
            refresh()
            return self.send_json(scraper.load())
        self.send_error(404)

    def send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):  # keep the console quiet except for errors
        if args and str(args[1])[0] in "45":
            super().log_message(fmt, *args)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--interval", type=int, default=30, help="minutes between automatic refreshes")
    args = ap.parse_args()

    threading.Thread(target=refresh_forever, args=(args.interval,), daemon=True).start()
    print(f"AI news on http://localhost:{args.port}  (refreshing every {args.interval} min)")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
