from flask import Blueprint
from flask import render_template
from flask import redirect, url_for
from flask import request
from vs_url_for import vs_url_for
from flask_login import current_user
from flask_login import LoginManager, login_required
from forms import addTwitForm, editTwitForm
from dbhelper import db

twits_blueprint = Blueprint('twits_blueprint', __name__,
                        template_folder = 'templates')

@twits_blueprint.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mysql.html", twits=twits)

@twits_blueprint.route('/add_twit', methods = ['GET', 'POST'])
@login_required
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        user_id = current_user.user_id
        db.add_twit(twit,user_id)
        return redirect(vs_url_for('.index'))
    return render_template('add_twit_mysql.html',form=form)

@twits_blueprint.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.get_twit(twit_id)
        form.twit.data = twit['twit']
        form.twit_id.data = twit_id
        return render_template('edit_twit_mysql.html',form=form,twit=twit)
    if form.validate_on_submit():
        twit = form.twit.data
        twit_id = form.twit_id.data
        db.update_twit(twit,twit_id)
        return redirect(vs_url_for('.index'))
    return render_template('edit_twit_mysql.html',form=form)

@twits_blueprint.route('/delete_twit', methods = ['GET', 'POST'])
@login_required
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.delete_twit(twit_id)
    return redirect(vs_url_for('.index'))
