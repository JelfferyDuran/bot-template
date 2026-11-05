"""Demo health endpoint: runs one poll cycle against a fake feed and reports
how many items were new vs already seen — the template's dedupe, live."""
from http.server import BaseHTTPRequestHandler
import json

SAMPLE = [
    {"id": "demo-1", "title": "Sample bounty: Discord moderation bot"},
    {"id": "demo-2", "title": "Sample bounty: Telegram appointment bot"},
    {"id": "demo-3", "title": "Sample bounty: price-drop scraper"},
]
SEEN = {"demo-1"}  # pretend one was already alerted


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        new = [i for i in SAMPLE if i["id"] not in SEEN]
        body = json.dumps({
            "status": "ok",
            "template": "bot-template",
            "poll": {"checked": len(SAMPLE), "new": len(new),
                     "already_seen": len(SEEN)},
            "new_items": new,
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
