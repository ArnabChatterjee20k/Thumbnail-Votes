from celery import Celery, Task
import sys,os

# sys.path.append(os.getcwd())
from thumnbail import create_app
# the app context must be pushed inside the create_app as we are using the create_app to create the celery worker
# celery = Celery(__name__,broker=CELERY_BROKER_BACKEND,backend=CELERY_RESULT_BACKEND)
app = create_app()
celery_app:Celery = app.extensions["celery"]