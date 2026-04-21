import os
import re
import requests
from pathlib import Path

URL = "https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html"
STATE_FILE = Path("state.txt")
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_skus():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return set(re.findall(r'VEP\d{4}', r.text))


def load_state():
    if not STATE_FILE.exists():
        return None
    return set(STATE_FILE.read_text().splitlines())


def save_state(skus):
    STATE_FILE.write_text("\n".join(sorted(skus)))


def notify(skus):
    for sku in sorted(skus):
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": f"Nouveau produit Legami : {sku}\n{URL}"},
            timeout=10,
        )


current = fetch_skus()
previous = load_state()

if previous is None:
    save_state(current)
else:
    new = current - previous
    if new:
        notify(new)
    save_state(current)
