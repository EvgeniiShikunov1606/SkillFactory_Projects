from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'board.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=0, minute=0, day_of_week='thursday'),
    },
}

app.conf.worker_max_tasks_per_child = 100
app.conf.worker_hard_time_limit = 300
