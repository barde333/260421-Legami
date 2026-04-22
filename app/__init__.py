from app.db import init_db
from app.scheduler import start_scheduler

init_db()
start_scheduler()
