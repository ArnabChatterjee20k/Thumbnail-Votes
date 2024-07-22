from votes import create_app , socketio
from dotenv import load_dotenv
load_dotenv(".env")
app = create_app()
app.app_context().push()
@app.get("/health")
def health():
    return "Vote service running"
socketio.run(app=app,host='0.0.0.0', port=5000,debug=True,allow_unsafe_werkzeug=True)