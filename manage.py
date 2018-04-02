# what is used to start and stop the application
import os, sys

# get the file's current location and then append to the python path the level above it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# these allow us to server the application
from flask_script import Manager, Server
# import flask migrate
from flask_migrate import MigrateCommand
# import flask-restless for api
import flask_restless
# import database
from flask_newsmarkr import db
# import app
from flask_newsmarkr import app

# import models for endpoints
from articlepool.models import ArticlePool, LiveComment
from bookmark.models import Collection, Bookmark, Category
# from profile.models import
from social.models import Post, Comment
from user.models import User


# instantiate manger from that app
manager = Manager(app)

# can add commands to the manager - flags in command line
# flask_migrate commands:
# if starting for FIRST TIME: 'python manage.py db init'
# to migrate and upgrade:
    # first, 'python manage.py db migrate' - creates file with hash(version)
    # then 'python manage.py db upgrade'
        # or change database to previous state: 'python manage.py db downgrade'

manager.add_command('db', MigrateCommand)
# add 'runserver' command to start server
# 'python manage.py runserver'
manager.add_command('runserver', Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000))
))


# api manager
api_manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# api endpoints
api_manager.create_api(ArticlePool, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(LiveComment, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(Collection, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(Bookmark, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(Category, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(Post, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(Comment, methods=['GET', 'POST', 'PUT', 'DELETE'])
api_manager.create_api(User, methods=['GET', 'POST', 'PUT', 'DELETE'])


# run server using following command:
    # 'python manage.py runserver'
if __name__ == '__main__':
    manager.run()
