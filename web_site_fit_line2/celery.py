import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
app = Celery('web_site_fit_line2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

