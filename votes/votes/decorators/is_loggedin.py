import functools
from flask import request
from werkzeug.exceptions import Unauthorized

def is_loggedin(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        data = request.args
        email = data.get("email")
        if not email:
            return Unauthorized()
        return func(*args,**kwargs)
    return wrapper
