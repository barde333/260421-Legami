# 260421-Legami

## Overview

**Legami Pen Watcher** — detect when a new erasable pen is released on Legami's French site.

The problem: Legami releases new erasable pens every few weeks and they sell out fast. The "nouveauté" badge on the site stays for weeks, so it's unreliable as a signal. This project checks the [erasable pens page](https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html) twice a week, compares against a local history of known product SKUs, and sends a Telegram notification when a truly new SKU appears.

## Architecture & Stack

| Layer | Choice |
|---|---|
| Runtime | Python 3.12-slim (Docker) |
| Scraping | `requests` + `beautifulsoup4` (page is static HTML) |
| Product ID | SKU extracted from product URL (e.g. `VEP0074`) — stable across renames |
| State | Single `state.json` file mounted as volume |
| Notifications | Telegram Bot API (`sendMessage`) |
| Scheduling | Host cron on CT 103 — Monday & Thursday, 10:00 Paris |

Single one-shot script: fetch → parse SKUs → diff against state → notify new SKUs → rewrite state. No web server, no DB.

## DevOps

- Hosted on CT 103 (Docker host) under `/opt/legami-watcher/`.
- Container launched on schedule via host cron: `docker compose run --rm watcher`.
- First run uses a `--seed` flag to populate `state.json` without notifying.
- On scrape failure (HTTP error, empty result), the state file is **not** overwritten and an alert is sent to Telegram.
- Code pushed from Mac → CT 103 via `rsync`, and to GitHub in parallel.

## Security

- Repo is public; contains no secrets.
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` stored in `.env` on CT 103 only, never committed (`.env.example` provided).
- Container has no exposed ports (batch job only, no NPM proxy host).
- Outbound HTTPS only (Legami + Telegram API).
