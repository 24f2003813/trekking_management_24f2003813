from extensions import celery
from celery.schedules import crontab
from celery import Celery


celery.conf.beat_schedule = {
    'send-daily-reminder':{
        'task':'tasks.send_daily_reminders',
        'schedule': crontab(hour=0,minute=0),
    },
    'mark-completed-treks': {
        'task': 'tasks.mark_completed_treks',
        'schedule': crontab(minute='*'), 
    },
    "send-monthly-report": {
        "task": "tasks.send_monthly_report",
        "schedule": crontab(minute='*'),
    },
}
# hour=0, minute=0, day_of_month=1