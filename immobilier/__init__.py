from __future__ import absolute_import, unicode_literals

# import os

# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immobilier.settings')

# app = Celery('immobilier')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
