import html, json
from datetime import datetime, timezone
from pathlib import Path

manifest = Path("events.json")
if not manifest.exists():
    raise SystemExit(0)
events = json.loads(manifest.read_text(encoding="utf-8"))
now = datetime.now(timezone.utc)
changed = False
for item in events:
    expiry = datetime.fromisoformat(item["expires_utc"].replace("Z", "+00:00"))
    target = Path("site") / item["slug"] / "index.html"
    if expiry <= now and item.get("status") != "expired":
        title = html.escape(item.get("title", "Event schedule"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex,nofollow,noarchive'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Schedule expired</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#071d36;color:white;font-family:Arial,sans-serif;text-align:center;text-transform:uppercase}main{padding:40px}h1{color:#14a8e0}</style></head><body><main><h1>Event schedule expired</h1><p>" + title + "</p><p>This link is no longer active.</p></main></body></html>", encoding="utf-8")
        item["status"] = "expired"
        changed = True
if changed:
    manifest.write_text(json.dumps(events, indent=2), encoding="utf-8")
