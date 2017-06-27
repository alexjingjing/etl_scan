from datetime import timedelta
from celery import Celery


app = Celery()
app.config_from_object('app.conf.celeryconfig')
