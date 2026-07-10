from celery import Celery,Task
from celery.schedules import crontab
from app import app

celery_app=Celery('task',broker='redis://localhost:6379/1', backend='redis://localhost:6379/2' , include=['tasks'])

celery_app.conf.beat_schedule = {
    'send-daily-reminder':{
        'task':'tasks.send_daily_reminders',
        'schedule': crontab(hour=0,minute=0),
    },
    'mark-completed-treks': {
        'task': 'tasks.mark_completed_treks',
        'schedule': crontab(hour=0,minute=0), 
    },
}