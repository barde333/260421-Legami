# Pathfinder — 260421-Legami

Numbered list of design & build steps. Model recommendation, token estimate, and status per step.

**Simplified plan** — single Python script, no Docker, host crontab on CT 103. Regex parsing (no BeautifulSoup), plain-text state file, implicit first-run seeding.

| # | Step | Description | Model | Tokens | Status |
|---|------|-------------|-------|--------|--------|

| 1 | Write `check.py` | Single ~40-line script: fetch page with realistic User-Agent, extract SKUs via `re.findall(r'VEP\d{4}', html)`, diff against `state.txt` (one SKU per line), POST new ones to Telegram `sendMessage`. If `state.txt` doesn't exist → write without notifying (implicit seed) | Sonnet | ~5k | ✅ Done |

| 2 | Repo scaffolding | `requirements.txt` (just `requests`), `.gitignore` (`.env`, `state.txt`), `.env.example` with `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Haiku | ~1k | ✅ Done |

| 3 | Deploy to CT 103 | `rsync` script to `/opt/legami-watcher/`, create `.env` with real secrets, `pip install -r requirements.txt --user`, first manual run to seed `state.txt` | Haiku | ~2k | ✅ Done |

| 4 | Crontab + verify | Add crontab entry on CT 103: Monday & Thursday 10:00 Europe/Paris. Test end-to-end by removing one SKU from `state.txt` and running manually → confirm Telegram notification | Haiku | ~2k | ✅ Done |

**Total estimate:** ~10k tokens (down from 33k). Simpler = cheaper, faster, less to maintain.

**Runtime cost:** 0 tokens. Once deployed, the script runs autonomously on CT 103 — Claude is not involved.

**Status legend:** ⏳ Todo · 🚧 In progress · ✅ Done · ⚠️ Blocked
