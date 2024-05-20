from flask import Flask , request
from utils import create_token,decode_token  , save_user , get_user , get_hash_password, decode_password
from db import create_db
app = Flask(__name__)
@app.post("/register")
def register():
    data = request.json
    is_user_exists = get_user(data["email"])
    if is_user_exists:
        return {"status":"user exists"},400

    save_user(data["name"],data["email"],get_hash_password(data["password"]))

    return {"token":create_token(data["email"])}
create_db()
app.run(debug=True,host="0.0.0.0",port=5000)