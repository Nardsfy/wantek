from flask import redirect, url_for
from flask_login import current_user
from functools import wraps

def login_not_allowed(fn):
    """ Redirect to homepage if user already authenticated """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if (current_user.is_authenticated):
            return redirect(url_for("home"))
        return fn(*args, **kwargs)
    return wrapper