# contains author decorators
from functools import wraps
from flask import session, request, redirect, url_for, abort

# create decorators for login authentication
# subclass f
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if user is not logged in
        if session.get('username') is None:
            # redirect to login, but maintain history of page you tried to hit, so that after logging in, the user is sent back to the url they tried to view originally
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# must be author
def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if user is not logged in
        if session.get('is_author') is None:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
