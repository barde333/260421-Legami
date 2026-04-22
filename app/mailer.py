import os
import httpx

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "noreply@pennino.bard3.duckdns.org")
SENDER_NAME = "Pennino — Legami Watcher"
SITE_URL = os.environ.get("SITE_URL", "https://pennino.bard3.duckdns.org")

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="fr">
<body style="font-family:sans-serif;max-width:480px;margin:auto;color:#222">
  <h2 style="color:#e63946">Nouveaux stylos Legami détectés ✏️</h2>
  <p>Les références suivantes viennent d'apparaître sur le site Legami :</p>
  <ul>
    {sku_items}
  </ul>
  <p>
    <a href="https://www.legami.com/fr-fr/papeterie/ecriture/stylos-effacables.html"
       style="background:#e63946;color:#fff;padding:10px 20px;text-decoration:none;border-radius:4px">
      Voir sur Legami →
    </a>
  </p>
  <hr style="margin-top:32px;border:none;border-top:1px solid #eee">
  <p style="font-size:12px;color:#999">
    Vous recevez cet email car vous vous êtes inscrit(e) sur Pennino.<br>
    <a href="{unsub_url}" style="color:#999">Se désinscrire</a>
  </p>
</body>
</html>
"""


def _unsub_url(token: str) -> str:
    return f"{SITE_URL}/unsubscribe?token={token}"


def send_alert(email: str, token: str, new_skus: list[str]) -> None:
    sku_items = "\n    ".join(f"<li>{sku}</li>" for sku in new_skus)
    html = HTML_TEMPLATE.format(sku_items=sku_items, unsub_url=_unsub_url(token))

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": email}],
        "subject": f"{len(new_skus)} nouveau(x) stylo(s) Legami détecté(s)",
        "htmlContent": html,
    }

    r = httpx.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
        timeout=10,
    )
    r.raise_for_status()
