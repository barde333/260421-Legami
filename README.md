# 260421-Legami

## Overview

**Legami Pen Watcher** — detect when a new erasable pen is released on Legami's French site.

The problem: Legami releases new erasable pens every few weeks and they sell out fast. The "nouveauté" badge on the site stays for weeks, so it's unreliable as a signal. This project checks the [erasable pens page](https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html) twice a week, compares against a local history of known product SKUs, and sends a Telegram notification when a truly new SKU appears.

## Architecture & Stack

| Layer | Choice |
|---|---|
| Runtime | Python 3 (system interpreter on CT 103) |
| Dependencies | `requests` only (installed via `apt install python3-requests`) |
| Scraping | `re.findall(r'VEP\d{4}', html)` on raw HTML — page is static |
| Product ID | SKU from URL (e.g. `VEP0074`), stable across renames |
| State | `state.txt`, one SKU per line |
| Notifications | Telegram Bot API (`sendMessage`) |
| Scheduling | Host crontab on CT 103, Monday & Thursday 10:00 Europe/Paris (`CRON_TZ`) |

Single ~40-line script `check.py`: fetch → regex SKUs → diff against state → notify new ones → rewrite state. First run writes state without notifying (implicit seed).

## DevOps

- Deployed at `/opt/legami-watcher/` on CT 103 (192.168.2.64).
- Crontab entry:
  ```
  CRON_TZ=Europe/Paris
  0 10 * * 1,4 cd /opt/legami-watcher && set -a && . ./.env && set +a && /usr/bin/python3 check.py >> /opt/legami-watcher/cron.log 2>&1
  ```
- No Docker, no reverse proxy, no exposed port — pure batch job.
- Code is pushed to GitHub from the Mac; CT 103 holds the runtime copy + `.env` + `state.txt`.

## Security

- Public repo, no secrets committed.
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` live in `/opt/legami-watcher/.env` on CT 103 only (see `.env.example`).
- `.env` and `state.txt` are gitignored.
- Outbound HTTPS only (Legami + Telegram API), no inbound traffic.
