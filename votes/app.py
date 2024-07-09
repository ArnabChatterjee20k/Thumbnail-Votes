from votes import create_app , socketio
app = create_app()
@app.get("/health")
def health():
    return "Vote service running"
socketio.run(app=app,host='0.0.0.0', port=5000,debug=True,allow_unsafe_werkzeug=True)