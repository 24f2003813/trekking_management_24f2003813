import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

DEBUG=True

CACHE_TYPE = 'RedisCache'
CACHE_REDIS_URL = 'redis://localhost:6379/0'


CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
