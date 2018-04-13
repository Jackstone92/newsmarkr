from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymysql

class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='mytwits_user',
            passwd='mytwits_password',
            db='mytwits')

    def get_all_twits(self):
        query = "select u.username, t.twit, t.created_at from twits t, users u where t.user_id=u.user_id order by t.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def validate_user(self, username, password):
        query_user = "SELECT EXISTS (SELECT * FROM login_details WHERE username = %s AND password = %s)"

        db_user = ''
        db_username = ''
        db_password = ''

        with self.db.cursor() as cursor:
            db_user = cursor.execute(query_user, (username, password))

        if db_user != '':
            print(db_user)
        else:
            print('user not found!')


        if db_username != '' and db_password != '':
            if db_username == username and db_password == password:
                return true
            else:
                print('username and password do not match!')
        else:
            print('username and password not found in db!')
            return false
