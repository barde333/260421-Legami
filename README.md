# 260421-Legami

## Overview

**Legami Pen Watcher** — micro-site public qui prévient par email les fans de stylos effaçables Legami dès qu'une nouvelle référence apparaît sur le site français.

Le problème : Legami sort des nouveaux stylos effaçables toutes les quelques semaines et ils partent vite. Le badge "nouveauté" reste des semaines sur le site → signal inutilisable. Ce projet scrute la [page stylos effaçables](https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html) chaque matin, compare à un historique local de SKUs connus, et envoie un email aux inscrits dès qu'un nouveau SKU apparaît.

Le site est hébergé sur `pennino.bard3.duckdns.org`.

## Architecture & Stack

| Couche | Choix |
|---|---|
| Runtime | Python 3 (container Docker unique) |
| Web | FastAPI + Jinja2 |
| Scraping | `re.findall(r'VEP\d{4}', html)` sur le HTML brut — page statique |
| Identifiant produit | SKU depuis l'URL (ex. `VEP0074`), stable malgré les renommages |
| Base de données | SQLite (inscrits + SKUs connus) |
| Scheduler | APScheduler en process, cron interne 10h Europe/Paris |
| Email | Resend (API transactionnelle) |
| Hébergement | Docker sur Proxmox CT, reverse proxy Nginx Proxy Manager |
| Langue | Français uniquement |

Un seul service Python : page d'inscription + endpoint de désinscription (token unique par inscrit) + job quotidien de scraping qui envoie les mails en batch via Resend.

## Fonctionnement utilisateur

1. Visite de `pennino.bard3.duckdns.org` → formulaire email.
2. L'utilisateur saisit son email → inscription immédiate (pas de double opt-in).
3. Chaque matin ~10h, si un nouveau stylo est détecté, tous les inscrits reçoivent un email avec le nom du produit et un lien vers la page Legami.
4. Chaque email contient un lien de désinscription (token unique) qui supprime l'adresse de la base.

## DevOps

- Déployé en container Docker sur Proxmox (skill Docker habituelle).
- Sous-domaine `pennino.bard3.duckdns.org` via Nginx Proxy Manager.
- Secrets (`RESEND_API_KEY`, clé de signature des tokens) dans `.env` monté dans le container, jamais committés.
- État persisté dans un volume : base SQLite (inscrits + SKUs connus).

## Sécurité & RGPD

- Repo public, aucun secret committé.
- HTTPS via NPM + Let's Encrypt.
- Lien de désinscription fonctionnel dans chaque email (obligation RGPD minimale).
- Pas de double opt-in, pas de mentions légales formelles, pas d'anti-spam dans la V2 initiale — à ajouter si le service prend de l'ampleur.

## Hors périmètre V2

Reportés à une version ultérieure :
- Internationalisation (EN/IT) avec sélecteur de langue
- Section « Dernier stylo détecté » sur la home (nécessite enrichissement du scraper : nom, prix, image)
- Dark mode
- Pourboire Stripe
- Page admin / statistiques
- Double opt-in, CAPTCHA, mentions légales complètes
- Préférences utilisateur (filtres par couleur, modèle, etc.)

## Historique

La V1 était un script Python minimaliste qui envoyait des notifications Telegram personnelles deux fois par semaine. Pour voir cet état : `git checkout v1-telegram`.
