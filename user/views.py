# import app from root (from __init__.py)
from flask_newsmarkr import app
from flask import render_template, redirect, url_for, session, request

# import login and signup forms from form.py
from user.form import SignupForm, LoginForm
# user.models to check in database

# import bcrypt to unhash password
import bcrypt

# import custom decorators
from user.decorators import login_required


@app.route('/')
def index():
    return 'hello world!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    # if got next url data from @login_required decorator
    if request.method == 'GET' and request.args.get('next'):
        # store as session
        session['next'] = request.args.get('next', None)

    # if form submitted
    if form.validate_on_submit():
        # database lookup - SELECT
        user = User.query.filter_by(
            # check for users with username entered
            username=form.username.data
        ).first() # returns first user

        # if user record found with username
        if user:
            # if encrypted form password is same hash as hashed author password on database, we have found the right user
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                # create flask login session
                session['username'] = form.username.data
                # store is_admin flag in session
                session['is_admin'] = user.is_admin
                # if have 'next' url in session -> navigate to next after login
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    # go straight to index
                    return redirect(url_for('index'))
            else:
                error = "Incorrect username and password"
        else:
            error = "Incorrect username and password"
    return render_template('user/login.html', form=form, error=error)
