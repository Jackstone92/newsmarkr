from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session, flash, abort
from flask import jsonify
from vs_url_for import vs_url_for
from forms import addTwitForm, editTwitForm, loginForm
from dbhelper import DBHelper
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from user import User

login_manager = LoginManager()

app = Flask(__name__)
db = DBHelper()
login_manager.init_app(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@login_manager.user_loader
def load_user(user_id):
    result = db.get_user(user_id)
    if result:
        return User(user_id)

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mysql.html", twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
@login_required
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        db.add_twit(twit,session['user_id'])
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mysql.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.get_twit(twit_id)
        form.twit.data = twit[0]
        form.twit_id.data = twit_id
        return render_template('edit_twit_mysql.html',form=form,twit=twit)
    if form.validate_on_submit():
        twit = form.twit.data
        twit_id = form.twit_id.data
        db.update_twit(twit,twit_id)
        return redirect(vs_url_for('index'))
    return render_template('edit_twit_mysql.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
@login_required
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.delete_twit(twit_id)
    return redirect(vs_url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user_id = db.check_password(username,password)
        if user_id:
            user = User(user_id)
            login_user(user)
            flash('login successful!')
            return redirect(vs_url_for('index'))
        else:
            flash('login unsuccessful!')
    return render_template('login.html',form=form)

@app.route('/api')
@app.route('/api/<username>')
def api(username=None):
    if username:
        twits = db.get_user_twits(username)
        return jsonify({'twits':twits})
    else:
        twits = db.get_all_twits()
        return jsonify({'twits':twits})

@app.route('/logout')
def logout():
    # remove username from session if there
    logout_user()
    return redirect(vs_url_for('index'))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
