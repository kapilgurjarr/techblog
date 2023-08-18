from celery import Celery
import os

#set the default django setting module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','techblog.settings')


app=Celery('techblog')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    pass
    # print(f'Request': {self.request!r})