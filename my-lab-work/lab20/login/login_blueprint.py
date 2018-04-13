from flask import Blueprint
from forms import loginForm
from flask import render_template
from flask import redirect, url_for
from flask import flash
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from flask_login import current_user
from user import User
from vs_url_for import vs_url_for
from dbhelper import db

login_manager = LoginManager()

login_blueprint = Blueprint('login_blueprint', __name__,
                        template_folder = 'templates')

@login_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_manager.user_loader
def load_user(user_id):
    result = db.get_user(user_id)
    if result:
        username = result[1]
        return User(user_id,username)


@login_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user_id = db.check_password(username,password)
        if user_id:
            user = User(user_id, username)
            login_user(user)
            return redirect(vs_url_for('twits_blueprint.index'))
        else:
            flash('login unsuccessful!')
    return render_template('login/login.html',form=form)


@login_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(vs_url_for('twits_blueprint.index'))
