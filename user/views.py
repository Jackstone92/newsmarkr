# import app from root (from __init__.py)
from flask_newsmarkr import app
from flask import render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from flask_newsmarkr import db
# import login and signup forms from form.py
from user.form import SignupForm, LoginForm
# user.models to check in database
from user.models import User

from utils.vs_url_for import vs_url_for


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
            # using werkzeug.security
            if check_password_hash(user.password, form.password.data):
                # flask_login
                login_user(user, remember=True)
                # create flask login session
                session['username'] = form.username.data
                # store is_admin flag in session
                if user.is_admin:
                    session['is_admin'] = user.is_admin
                # if have 'next' url in session -> navigate to next after login
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    # go straight to index
                    return redirect(vs_url_for('social'))
            else:
                error = "Incorrect username and password"
        else:
            error = "Incorrect username and password"
    return render_template('user/login.html', form=form, error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # instantiate form
    form = SignupForm()
    # set up blank error
    error = None
    # check form was submitted - checks that form didn't have any errors (from validators)
    if form.validate_on_submit():
        # using werkzeug.security
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # create a user from those form records
        user = User(
            # access form data by .data
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            str(vs_url_for('static', filename='images/profile_picture.png')),
            None,
            str(vs_url_for('static', filename='images/newspaper.jpg')),
            None,
            True
        )
        # add to database
        db.session.add(user)
        # flush - sqlalchemy simulates that record is written, and provide id etc. However, doesn't hit database yet - can always throw back
        db.session.flush()
        # if we have user id - validation
        if user.id:
            # actually commit transaction to database
            db.session.commit()
            # redirect to user login
            return redirect(vs_url_for('login'))
        else:
            # undo flush by rollback()
            db.session.rollback()
            error = "Error creating user"
            flash(error)

    # render template and pass in form
    return render_template('user/signup.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    # flask_login
    logout_user()
    session.pop('username')
    session.pop('is_admin')
    return redirect(vs_url_for('index'))
