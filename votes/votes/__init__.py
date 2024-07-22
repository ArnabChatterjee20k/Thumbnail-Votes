from flask import Flask
from flask_socketio import SocketIO
from .db import create_db
from .models import *
from votes.workers.BgWorkers import create_bg_workers
from kombu import Exchange,Queue
import os

socketio = SocketIO(cors_allowed_origins='*')
CELERY_BROKER_BACKEND = os.environ.get("AMQP_URI")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

def create_app():
    from votes.workers.schedule_emit import emit_to_rooms
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config.from_mapping(
        CELERY=dict(
            broker_url=CELERY_BROKER_BACKEND,
            task_track_started=True,
            celery_imports=("votes.workers",),
            task_queues=(
            Queue('default', Exchange('default'), routing_key='default'),
            Queue('scheduler_queue', Exchange('scheduler_queue'), routing_key='scheduler_queue'),
        ),
        )
    )
    create_db()
    from votes.routes import main
    app.register_blueprint(main)
    socketio.init_app(app=app)
    create_bg_workers(app)
    app.app_context().push()
    return app