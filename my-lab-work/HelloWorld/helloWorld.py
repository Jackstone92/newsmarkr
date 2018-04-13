from flask import Flask
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/date')
def get_date():
	return 'The current date is: ' + str(datetime.datetime.now())

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=8000)
