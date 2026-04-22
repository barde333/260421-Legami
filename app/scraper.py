import re
import httpx
from app.db import get_conn

URL = "https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_skus() -> set[str]:
    r = httpx.get(URL, headers=HEADERS, timeout=15, follow_redirects=True)
    r.raise_for_status()
    return set(re.findall(r"VEP\d{4}", r.text))


def scrape_and_diff() -> list[str]:
    """
    Fetch current SKUs, persist new ones, return list of new SKUs.
    On first run (empty table) silently seeds the DB and returns [].
    """
    current = fetch_skus()

    with get_conn() as conn:
        existing = {row["sku"] for row in conn.execute("SELECT sku FROM known_skus")}
        new_skus = current - existing

        if new_skus:
            conn.executemany(
                "INSERT OR IGNORE INTO known_skus (sku) VALUES (?)",
                [(sku,) for sku in new_skus],
            )

        if not existing:
            # First run: seed silently
            return []

    return sorted(new_skus)
