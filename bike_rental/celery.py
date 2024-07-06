import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bike_rental.settings')

app = Celery('bike_rental')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()