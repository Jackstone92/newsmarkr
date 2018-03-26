from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from flask_newsmarkr import db


@app.route('/social', methods=['GET', 'POST'])
def social():
    return render_template('social/social.html')
