# import app from root (from __init__.py)
from flask_newsmarkr import app
from flask import render_template, redirect, url_for, session, request, flash

from flask_newsmarkr import db
# import login and signup forms from form.py
from user.form import SignupForm, LoginForm
# user.models to check in database
from user.models import User
from bookmark.models import Library

# import bcrypt to unhash password
import bcrypt

# import custom decorators
from user.decorators import login_required


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
                    return redirect(url_for('library'))
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
        # generate salt (random hash used to generate new password)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)

        # create a user from those form records
        user = User(
            # access form data by .data
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True
        )

        # add to database
        db.session.add(user)
        # flush - sqlalchemy simulates that record is written, and provide id etc. However, doesn't hit database yet - can always throw back
        db.session.flush()
        # if we have user id - validation
        if user.id:
            # build a library object and pass in user id as foreign key
            library = Library(
                form.name.data,
                user.id
            )
            # add library to database
            db.session.add(library)
            db.session.flush()
        else:
            # undo flush by rollback()
            db.session.rollback()
            error = "Error creating user"

        # check both before committing to db
        if user.id and library.id:
            # actually commit transaction to database
            db.session.commit()
            # if success, flash
            flash("Newsmarkr Library Created!")
            # redirect to user library
            return redirect(url_for('login'))
        else:
            # rollback
            db.session.rollback()
            error = "Error creating Newsmarkr library"
            flash(error)

    # render template and pass in form
    return render_template('user/signup.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('username')
    session.pop('is_admin')
    return redirect(url_for('index'))
