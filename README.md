# bot-template

A generic polling bot starter: **poll a source, dedupe what it already saw, alert on what's new** — with multi-server config wired in. Fork it per bounty, point it at the real source, ship.

**Live demo:** https://bot-template-kingdom-noel.vercel.app

## What's inside

- `bot/poller.py` — polls a source function on an interval, yields only new items
- `bot/dedupe.py` — `SeenStore`: JSON-backed set of seen ids, survives restarts
- `bot/alerts.py` — alert sinks: console + webhook POST (add your own by matching `send_alert`)
- `bot/config.py` — multi-server config from `config/servers.json` or `SERVERS_JSON`
- `bot/server.py` — stdlib `/health` endpoint so the bot proves it runs
- `bot/main.py` — wires it all together; `--demo` runs on a fake source with no setup
- `demo/` — the live demo site (static page + `/api/health`)

## Quickstart

```bash
python3 -m unittest discover -s tests -v   # tests pass with zero setup
python3 -m bot.main --demo --once          # one demo cycle, no tokens needed
python3 -m bot.main --demo                 # keep polling (Ctrl-C to stop)
```

## Fork it per bounty (15–30 min)

1. Fork the repo.
2. Copy `config/servers.example.json` to `config/servers.json` and set each server's `source_url` + `alert_webhook_url`.
3. Replace `demo_source` in `bot/main.py` with your real fetch — or just set a JSON feed URL and use the built-in `json_feed_source`.
4. Add the bounty platform's library to `requirements.txt` (e.g. `discord.py`, `python-telegram-bot`).
5. Smoke-test: `python3 -m bot.main --once --demo`, then run for real.

## Config

Each server in `config/servers.json`:

```json
{
  "name": "my-server",
  "source_url": "https://example.com/api/items",
  "poll_interval_seconds": 60,
  "alert_webhook_url": "https://example.com/hooks/alerts",
  "channel": "#alerts"
}
```

Leave `source_url` empty to use the demo source. Or skip the file entirely and set `SERVERS_JSON` to the same JSON.

## Notes

- Python 3.10+, standard library only — no dependencies to install.
- Never commit real tokens: use `.env` (see `.env.example`) and `config/servers.json` (gitignored).
- This is a starter, not a guarantee: it doesn't promise any bounty, application, or earnings.
