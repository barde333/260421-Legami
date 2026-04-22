import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


def _daily_job():
    from app.scraper import scrape_and_diff
    from app.mailer import send_alert
    from app.db import get_conn

    new_skus = scrape_and_diff()
    if not new_skus:
        logger.info("Aucun nouveau SKU détecté.")
        return

    logger.info("Nouveaux SKUs : %s", new_skus)

    with get_conn() as conn:
        subscribers = conn.execute("SELECT email, token FROM subscribers").fetchall()

    for row in subscribers:
        try:
            send_alert(row["email"], row["token"], new_skus)
            logger.info("Email envoyé à %s", row["email"])
        except Exception:
            logger.exception("Erreur envoi email à %s", row["email"])


def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Europe/Paris")
    scheduler.add_job(
        _daily_job,
        CronTrigger(hour=10, minute=0, timezone="Europe/Paris"),
        id="daily_scrape",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler démarré — job quotidien à 10:00 Europe/Paris")
    return scheduler
