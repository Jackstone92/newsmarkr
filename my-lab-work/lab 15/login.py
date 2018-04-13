# pip imports
from flask import Flask, render_template
from flask import request, flash
import string
from flask_wtf import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators

# custom imports
from db import DBHelper



class LoginForm(Form):
    username = StringField('username', validators = [validators.DataRequired()])
    password = PasswordField('password', validators = [validators.DataRequired(), validators.length(min=8)])
    password2 = PasswordField('password2', validators = [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [validators.DataRequired()])


app = Flask(__name__)

USERNAME, PASSWORD = 'jimmy', '12345'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def clean_string(user_input):
    # return element if alphanumeric
    return ''.join(e for e in user_input if e.isalnum())



@app.route('/')
def index():
    return render_template('index.html');


@app.route('/login', methods=['GET', 'POST'])
def login():
    username, password = '', ''
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        if username == USERNAME and password == PASSWORD:
            flash('login successful!')
            session['user_id'] = user_id
    return render_template('mock_login_wtforms.html', form=login_form)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
