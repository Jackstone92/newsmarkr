# start up and app creation handling

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# add flask-migrate
from flask_migrate import Migrate

app = Flask(__name__)
# set configuration from settings file
app.config.from_object('settings')
# accessible db instance of sqlalchemy (holds database)
db = SQLAlchemy(app)

# Migrations
# pass app and db
migrate = Migrate(app, db)


# import all views (controllers)
from user import views
from bookmark import views
from articlepool import views
from profile import views
from social import views
