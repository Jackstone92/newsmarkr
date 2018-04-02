# start up and app creation handling

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless
# add flask-migrate
from flask_migrate import Migrate
# import flask-markdown
from flaskext.markdown import Markdown
# import flask-uploads
from flask_uploads import UploadSet, configure_uploads, IMAGES
# import flask-socketIO
from flask_socketio import SocketIO, emit


app = Flask(__name__)
# set configuration from settings file
app.config.from_object('settings')
# accessible db instance of sqlalchemy (holds database)
db = SQLAlchemy(app)

# Migrations
# pass app and db
migrate = Migrate(app, db)


# Markdown
Markdown(app)

# flask_uploads
uploaded_images = UploadSet('images', IMAGES)
configure_uploads(app, uploaded_images)

# flask-socketIO
socketio = SocketIO(app)


# import all views (controllers)
from user import views
from bookmark import views
from articlepool import views
from profile import views
from social import views
