# Pathfinder — V2 Legami Pen Watcher

Étapes de conception & build de la V2 : micro-site public FR + notifications email quotidiennes.
La V1 (script Telegram) est archivée sous le tag git `v1-telegram`.

**Stack simplifiée** : Flask (3 routes) + Brevo (API transactionnelle, sender vérifié par email — pas besoin de domaine) + SQLite stdlib + APScheduler. Un seul container Docker.

| # | Étape | Description | Modèle | Tokens | Statut |
|---|-------|-------------|--------|--------|--------|
| 1 | Préparation comptes | Créer compte Brevo (gratuit, 300 mails/jour) + ajouter sender vérifié par email (pas de DNS requis) + générer API key. Réserver sous-domaine `pennino.bard3.duckdns.org` dans DuckDNS | Haiku | ~1k | Done |
| 2 | Squelette repo | Structure `app/`, `templates/`, `Dockerfile`, `docker-compose.yml`, `requirements.txt` (flask, httpx, apscheduler), `.gitignore`, `.env.example` | Haiku | ~2k | Done |
| 3 | DB + scraping | `sqlite3` stdlib : tables `subscribers` et `known_skus`, init idempotente. `scraper.py` : fetch + regex `VEP\d{4}`, diff, insertion. Premier run = seed silencieux | Sonnet | ~4k | ⏳ |
| 4 | Mailer + scheduler | `mailer.py` : API Brevo (`POST /v3/smtp/email`, ~15 lignes), template HTML FR, lien désinscription avec token. APScheduler : job quotidien 10:00 Europe/Paris → scrape → envoi si nouveaux | Sonnet | ~4k | ⏳ |
| 5 | Micro-site Flask (routes) | `GET /` page + formulaire inscription, `POST /` traitement, `GET /unsubscribe?token=...` suppression. Templates Jinja, rendu FR | Sonnet | ~3k | ⏳ |
| 5b | Intégration design Pennino | Porter le HTML/CSS du prototype (`Pennino.html`) : rainbow stripe, nav+logo, pen-row animée, hero (eyebrow + H1 + sub + form email inline + hint), confirmation inline, footer. **Retirer** : switcher FR/EN/IT, tweaks panel, dark mode, section « Dernier stylo détecté », section « Comment ça marche » | Sonnet | ~4k | ⏳ |
| 6 | Packaging Docker | `Dockerfile` Python slim, `docker-compose.yml` avec volume `/data` et port 8000, conf via skill Docker du projet | Sonnet | ~3k | ⏳ |
| 7 | Déploiement Proxmox | Push code, config NPM (`pennino.bard3.duckdns.org` → :8000 + Let's Encrypt), volume monté, `.env` rempli, démarrage + vérif logs | Sonnet | ~3k | ⏳ |
| 8 | Bascule V1 → V2 | Vérifier scraping V2 cohérent avec V1, retirer cron Telegram sur CT 103, archiver `/opt/legami-watcher/` | Haiku | ~1k | ⏳ |
| 9 | Tests end-to-end | Inscription → forcer nouveau SKU → vérifier email reçu → clic désinscription → vérifier suppression. Contrôle anti-spam. Commit + merge `main` | Sonnet | ~2k | ⏳ |

**Total estimé :** ~27k tokens (ajout étape 5b intégration design)

**Runtime cost :** 0 tokens. Une fois déployée, l'app tourne seule en container Docker.

**Légende statut :** ⏳ À faire · 🚧 En cours · ✅ Fait · ⚠️ Bloqué

## Hors périmètre V2 (reportés)

- i18n EN + IT avec sélecteur manuel
- Section « Dernier stylo détecté » (nécessite scraper enrichi : nom, prix, image)
- Section « Comment ça marche »
- Dark mode
- Stripe Payment Link pour pourboires 1–5 €
- Mentions légales / politique de confidentialité
- Double opt-in, CAPTCHA
- Page stats / admin
- Passage à un domaine d'envoi dédié (DKIM/SPF) si déliverabilité insuffisante
