# Pathfinder — V2 Legami Pen Watcher

Étapes de conception & build de la V2 : micro-site public FR + notifications email quotidiennes.
La V1 (script Telegram) est archivée sous le tag git `v1-telegram`.

**Stack simplifiée** : Flask (3 routes) + Resend (API ultra simple) + SQLite stdlib + APScheduler. Un seul container Docker.

| # | Étape | Description | Modèle | Tokens | Statut |
|---|-------|-------------|--------|--------|--------|
| 1 | Préparation comptes & domaine | Créer compte Resend + vérifier domaine d'envoi (SPF/DKIM), réserver sous-domaine `pennino.bard3.duckdns.org` dans DuckDNS | Haiku | ~1k | ⏳ |
| 2 | Squelette repo | Structure `app/`, `templates/`, `Dockerfile`, `docker-compose.yml`, `requirements.txt` (flask, httpx, apscheduler), `.gitignore`, `.env.example` | Haiku | ~2k | ⏳ |
| 3 | DB + scraping | `sqlite3` stdlib : tables `subscribers` et `known_skus`, init idempotente. `scraper.py` : fetch + regex `VEP\d{4}`, diff, insertion. Premier run = seed silencieux | Sonnet | ~4k | ⏳ |
| 4 | Mailer + scheduler | `mailer.py` : API Resend (~10 lignes), template HTML FR, lien désinscription avec token. APScheduler : job quotidien 10:00 Europe/Paris → scrape → envoi si nouveaux | Sonnet | ~4k | ⏳ |
| 5 | Micro-site Flask | `GET /` page + formulaire inscription, `POST /` traitement, `GET /unsubscribe?token=...` suppression. Templates Jinja minimalistes, CSS simple | Sonnet | ~3k | ⏳ |
| 6 | Packaging Docker | `Dockerfile` Python slim, `docker-compose.yml` avec volume `/data` et port 8000, conf via skill Docker du projet | Sonnet | ~3k | ⏳ |
| 7 | Déploiement Proxmox | Push code, config NPM (`pennino.bard3.duckdns.org` → :8000 + Let's Encrypt), volume monté, `.env` rempli, démarrage + vérif logs | Sonnet | ~3k | ⏳ |
| 8 | Bascule V1 → V2 | Vérifier scraping V2 cohérent avec V1, retirer cron Telegram sur CT 103, archiver `/opt/legami-watcher/` | Haiku | ~1k | ⏳ |
| 9 | Tests end-to-end | Inscription → forcer nouveau SKU → vérifier email reçu → clic désinscription → vérifier suppression. Contrôle anti-spam. Commit + merge `main` | Sonnet | ~2k | ⏳ |

**Total estimé :** ~23k tokens (vs 30k avant coupes)

**Runtime cost :** 0 tokens. Une fois déployée, l'app tourne seule en container Docker.

**Légende statut :** ⏳ À faire · 🚧 En cours · ✅ Fait · ⚠️ Bloqué

## Hors périmètre V2 (reportés)

- i18n EN + IT avec sélecteur manuel
- Stripe Payment Link pour pourboires 1–5 €
- Mentions légales / politique de confidentialité
- Double opt-in, CAPTCHA
- Page stats / admin
- Migration Resend → Brevo si volume > 100 mails/jour
