from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
import dotenv
import environs

dotenv.load_dotenv()
env = environs.Env()
env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.dev')

app = Celery('eosform', broker=env.str('BROKER_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
