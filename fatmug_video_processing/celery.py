"""Celery configuration file."""

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatmug_video_processing.settings')  # Update with your project name

app = Celery('fatmug_video_processing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
