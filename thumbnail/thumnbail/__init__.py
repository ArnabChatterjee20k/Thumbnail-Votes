import os
from flask import Flask
from thumnbail.routes.router import router
from .db import create_db

from thumnbail.workers.BgWorkers import create_bg_workers
CELERY_BROKER_BACKEND = os.environ.get("AMQP_URI")


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=CELERY_BROKER_BACKEND, task_track_started=True,
            celery_imports = ("thumbnail.workers",)
        )
    )
    app.register_blueprint(router)
    create_db()
    create_bg_workers(app)
    app.app_context().push()
    return app
