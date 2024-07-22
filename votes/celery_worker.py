from celery import Celery, Task
import sys,os
from votes.services.VoteCache import vote_manager
# sys.path.append(os.getcwd())
from votes import create_app
# the app context must be pushed inside the create_app as we are using the create_app to create the celery worker
# celery = Celery(__name__,broker=CELERY_BROKER_BACKEND,backend=CELERY_RESULT_BACKEND)
app = create_app()
celery_app:Celery = app.extensions["celery"]
celery_app.conf.beat_schedule = {
    'emit-votes-to-room-every-30-seconds': {
        'task': 'votes.workers.schedule_emit.emit_to_rooms',
        'schedule': 30.0,
        'options': {'queue' : 'scheduler_queue'},
    },
}