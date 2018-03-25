from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

# from bookmark.form import SetupForm
from flask_newsmarkr import db
from user.models import User
from bookmark.models import Library, Bookmark, Category

# import bcrypt for password hashing
import bcrypt


@app.route('/')
@app.route('/index')
def index():
    return 'hello world!'


@app.route('/library')
def library():
    return 'welcome to the library'
