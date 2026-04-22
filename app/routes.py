import secrets
from flask import Blueprint, request, render_template, redirect, url_for
from app.db import get_conn

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/", methods=["POST"])
def subscribe():
    email = (request.form.get("email") or "").strip().lower()

    if not email or "@" not in email:
        return render_template("index.html", error="Adresse email invalide.")

    token = secrets.token_urlsafe(32)

    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM subscribers WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            return render_template("index.html", success=True, already=True)

        conn.execute(
            "INSERT INTO subscribers (email, token) VALUES (?, ?)",
            (email, token),
        )

    return render_template("index.html", success=True)


@bp.route("/unsubscribe")
def unsubscribe():
    token = request.args.get("token", "")

    if not token:
        return render_template("unsubscribe.html", error=True)

    with get_conn() as conn:
        row = conn.execute(
            "SELECT email FROM subscribers WHERE token = ?", (token,)
        ).fetchone()

        if not row:
            return render_template("unsubscribe.html", error=True)

        conn.execute("DELETE FROM subscribers WHERE token = ?", (token,))
        email = row["email"]

    return render_template("unsubscribe.html", email=email)
