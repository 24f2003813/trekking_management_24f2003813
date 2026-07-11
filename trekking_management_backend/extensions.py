from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery
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

celery.conf.update(app.config)