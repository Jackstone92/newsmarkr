# database operations

# must import main db
from flask_newsmarkr import db

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
class User(db.Model):
    # id is autoincrementing number, that increases with each new record
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True) # want only one user with same email per table
    username = db.Column(db.String(80), unique=True) # want only one user with same username per table
    password = db.Column(db.String(60)) # 60 chars for bcrypt hashed password standard
    image = db.Column(db.String(256))
    # create flag for permissions
    is_admin = db.Column(db.Boolean)

    # bookmarks relationship with user -> so that we can do bookmarks.user and get the bookmarks' user
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    post = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    live_comments = db.relationship('LiveComment', backref='user', lazy='dynamic')

    # constructor called when class is instantiated for first time
    def __init__(self, fullname, email, username, password, is_admin=False, image='https://www.communitylandtrust.ca/wp-content/uploads/2015/10/placeholder.png'):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.image = image

    # representation - how do you want to display this when interacting with it in, say, the terminal?
    def __repr__(self):
        return '<User %r>' % self.username
