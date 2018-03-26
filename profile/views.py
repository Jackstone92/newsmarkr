from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from flask_newsmarkr import db


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile/profile.html')
