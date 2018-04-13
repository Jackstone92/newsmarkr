# Settings file
import os

# best way to generate secret key: in python terminal, 'import os', then 'os.urandom(24)' -> results in random
SECRET_KEY = '\x01a\xd3\xf9E\xdbl.\x8a\xa9\x0es\xf8\x03\xdb\xf3(\xa8\xcb\xeb\xf7Y'
DEBUG = False

# database setup
DB_USERNAME = 'newsmarkr'
DB_PASSWORD = 'newsmarkr'
APP_DATABASE_NAME = 'newsmarkr'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, APP_DATABASE_NAME)

# required variable for sqlalchemy
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# for flask-uploads
# where images are saved on server (print pwd to get directory!)
UPLOADED_IMAGES_DEST = '/Users/jacksimac/Developer/Projects/flask_newsmarkr/flask_newsmarkr/static/uploads/images'
# how you serve images - prepend to images served
UPLOADED_IMAGES_URL = '/static/uploads/images/'
