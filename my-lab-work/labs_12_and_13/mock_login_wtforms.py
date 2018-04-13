from flask import Flask, render_template
from flask import request, flash
import string
from flask_wtf import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators

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


@app.route('/', methods=['GET', 'POST'])
def login():
    username, password = '', ''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == USERNAME and password == PASSWORD:
            flash('login successful!')
    list = [username, password]
    return render_template('mock_login_wtforms.html', list=list)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
