# Applying with this template

Copy-paste blurb for your next bot bounty application:

> I already have a working starter for this: a generic polling bot template
> (polling + dedupe + alerts + multi-server config) with a live demo — see
> the demo link at the top of the README.
> Repo: https://github.com/JelfferyDuran/bot-template
> For your bounty I'd fork it, point the poller at your source, and wire your
> alert channel — most of the plumbing is already done.

What to customize per bounty (15–30 min):

1. Fork the repo.
2. Copy `config/servers.example.json` to `config/servers.json`; set `source_url` + alert webhook.
3. Replace `demo_source` in `bot/main.py` with your real fetch (or set a JSON feed URL).
4. Run `python3 -m bot.main --once --demo` to smoke-test, then run for real.

No earnings or outcomes are promised — this is a starter, not a guarantee.
