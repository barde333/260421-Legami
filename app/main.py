from flask import Flask
from app.db import init_db
from app.scheduler import start_scheduler
from app.routes import bp


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.register_blueprint(bp)
    init_db()
    start_scheduler()
    return app


app = create_app()
