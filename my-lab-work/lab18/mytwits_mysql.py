from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session, flash, abort
from vs_url_for import vs_url_for
from forms import addTwitForm, editTwitForm, loginForm
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from flask_login import current_user
from models import db,Users,Twits
from passwordhelper import PasswordHelper

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.config['SQLALCHEMY_ECHO'] = False
db.init_app(app)
login_manager.init_app(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

ph = PasswordHelper()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    twits = Twits.query.order_by(Twits.created_at.desc()).all()
    return render_template("mytwits_mysql.html", twits=twits)

@app.route('/<username>')
def timeline(username):
    twits = Users.query.filter_by(username=username).first().twits
    return render_template('timeline.html',twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
@login_required
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        user_id = current_user.user_id
        new_twit = Twits(twit=twit, user_id=user_id)
        db.session.add(new_twit)
        db.session.commit()
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mysql.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    user_id = current_user.user_id
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = Twits.query.filter_by(twit_id = twit_id).first()
        form.twit.data = twit.twit
        form.twit_id.data = twit_id
        return render_template('edit_twit_mysql.html',form=form)
    if form.validate_on_submit():
        # get twit_id back from form
        twit_id = form.twit_id.data
        # load twit
        twit = Twits.query.filter_by(twit_id = twit_id).first()
        # change twit text to text submitted in form
        twit.twit = form.twit.data
        # commit change
        db.session.commit()
        return redirect(vs_url_for('index'))
    return render_template('edit_twit_mysql.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
@login_required
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit_for_deletion = Twits.query.filter_by(twit_id = twit_id).first()
        db.session.delete(twit_for_deletion)
        db.session.commit()
    return redirect(vs_url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        # get user object using sqlalchemy
        user = Users.query.filter_by(username=username).first()
        # use password helper to validate password
        if ph.validate_password(password,user.salt,user.hashed):
            login_user(user)
            return redirect(vs_url_for('index'))
        else:
            flash('please try again')
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    # remove username from session if there
    logout_user()
    return redirect(vs_url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
