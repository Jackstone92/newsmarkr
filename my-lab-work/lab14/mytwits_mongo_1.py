from flask import Flask, render_template
from flask import request, flash
import string
from flask_wtf import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
import pymongo


class DBHelper():

	def __init__(self):
		client = pymongo.MongoClient()
		self.db = client['mytwits']

	def get_all_twits(self):
		return self.db.twits.find().sort('created_at', pymongo.ASCENDING)


app = Flask(__name__)
db = DBHelper()

@app.route('/')
def index():
	twits = db.get_all_twits()
	return render_template('index.html', twits=twits)
