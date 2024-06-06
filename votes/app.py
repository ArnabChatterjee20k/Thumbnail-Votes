from votes import create_app , socketio
app = create_app()
socketio.run(app=app,debug=True)