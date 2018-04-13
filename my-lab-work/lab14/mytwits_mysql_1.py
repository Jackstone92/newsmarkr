from flask import Flask
from flask import make_response
from flask import render_template
from flask import request




class DBHelper():

	def __init__(self):
		self.db = pymysql.connect(host='localhost', user='username', password='password', db='mytwits')
