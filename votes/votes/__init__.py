from flask import Flask
from flask_socketio import SocketIO
from .db import create_db
from votes.routes.routes import router
socketio = SocketIO(cors_allowed_origins='*')
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.register_blueprint(router)
    create_db()
    socketio.init_app(app=app)
    return app

"""
    todo
    add support for updating votes and voters in the table using consumers
"""