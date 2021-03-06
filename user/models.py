# database operations

# must import main db
from flask_newsmarkr import db, login_manager

# from flask_login
from flask_login import UserMixin

# in order to add tables to database:
    # in terminal, type 'python manage.py shell'
    # import db into shell: 'from flask_newsmarkr import db'
    # import user models into shell: 'from user.models import *'
    # create database by calling 'db.create_all()'

# to add instance of user using 'python manage.py shell':
    # 'from flask_newsmarkr import db'
    # 'from user.models import *'
    # 'user = User('Jack Stone', 'test@test.com', 'jack', '12345', True)'
    # 'user' -> repr -> <User jack>
    # precommit to database (for multiple additions) - 'db.session.add(user)'
    # commit entries to database - 'db.session.commit()'

# to query entries:
    # return all in list:
        # 'users = User.query.all()'
        # 'users' -> [<User jack>, <User tessa>]
    # filter by:
        # 'users = User.query.filter_by(username='jack').first()'

# to remove all data from database:
    # COMMIT FIRST - 'db.session.commit()'
    # drop all tables: 'db.drop_all()'

# when sqlalchemy runs, it maps the columns to the properties of this class
class User(UserMixin, db.Model):
    """ Model for user """
    # id is autoincrementing number, that increases with each new record
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True) # want only one user with same email per table
    username = db.Column(db.String(25), unique=True) # want only one user with same username per table
    password = db.Column(db.String(80))
    profile_picture = db.Column(db.String(256))
    profile_picture_upload = db.Column(db.String(256))
    cover_photo = db.Column(db.String(256))
    cover_photo_upload = db.Column(db.String(256))
    # create flag for permissions
    is_admin = db.Column(db.Boolean)

    # bookmarks relationship with user -> so that we can do bookmarks.user and get the bookmarks' user
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    post = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    live_comments = db.relationship('LiveComment', backref='user', lazy='dynamic')

    # constructor called when class is instantiated for first time
    def __init__(self, fullname, email, username, password, profile_picture, profile_picture_upload, cover_photo, cover_photo_upload, is_admin=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.profile_picture = profile_picture
        self.profile_picture_upload = profile_picture_upload
        self.cover_photo = cover_photo
        self.cover_photo_upload = cover_photo_upload
        self.is_admin = is_admin

    # representation - how do you want to display this when interacting with it in, say, the terminal?
    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
