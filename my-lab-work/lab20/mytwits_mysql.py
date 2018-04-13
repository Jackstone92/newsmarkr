from flask import Flask
from twits_blueprint import twits_blueprint
from login.login_blueprint import login_blueprint
from flask_login import current_user

app = Flask(__name__)
app.register_blueprint(twits_blueprint)
app.register_blueprint(login_blueprint)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
