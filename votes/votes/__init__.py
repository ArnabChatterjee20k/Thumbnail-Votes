from flask import Flask
from flask_socketio import SocketIO
from .db import create_db

socketio = SocketIO(cors_allowed_origins='*')
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    create_db()
    socketio.init_app(app=app)
    return app

"""
    todo
    add a rabbitmq consumer for getting thumbnails are ready or not -> payload accepting {project_id:"",images_ids:[]}
    add a db support for adding thumbnails to the table
"""