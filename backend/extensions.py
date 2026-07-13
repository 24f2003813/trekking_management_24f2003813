from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
cache = Cache(app)

celery = Celery(
    app.import_name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
    include=["tasks"]
)

celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
)
celery.conf.beat_schedule = {
    "send-daily-reminder": {
        "task": "tasks.send_daily_reminders",
        "schedule": crontab(hour=0, minute=0),
    },
    "mark-completed-treks": {
        "task": "tasks.mark_completed_treks",
        "schedule": crontab(hour=0,minute=0),
    },
    "send-monthly-report": {
        "task": "tasks.send_monthly_report",
        "schedule": crontab(hour=0,minute=0),
    },
}

celery.conf.timezone = "Asia/Kolkata"
celery.conf.enable_utc = False