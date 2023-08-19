from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immobilier.settings')

app = Celery('immobilier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# worker_cancel_long_running_tasks_on_connection_loss = True


app.conf.beat_schedule = {
    'increase-user-balance': {
        'task': 'investisseurs.tasks.augmenter_solde',
        # 'schedule': crontab(hour=0, minute=00),  # Planifier tous les jours à 0h10
        'schedule': crontab(minute='*/5'),  # Planifier toutes les 5 minutes
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
