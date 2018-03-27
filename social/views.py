from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from flask_newsmarkr import db

from social.form import PostForm


@app.route('/social-feed', methods=['GET', 'POST'])
def social():
    form = PostForm()

    # if form.validate_on_submit()

    return render_template('social/social.html', form=form)
