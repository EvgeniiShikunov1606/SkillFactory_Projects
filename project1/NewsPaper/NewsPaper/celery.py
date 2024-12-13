from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=0, minute=0, day_of_week='thursday'),
    },
}

# app.conf.worker_max_tasks_per_child = 1000
# app.conf.worker_hard_time_limit = 600

CELERY_TASK_FORCE_EXECV = True
app.conf.worker_pool = 'solo'

