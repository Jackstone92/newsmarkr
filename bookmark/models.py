from flask_newsmarkr import db
from datetime import datetime

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    num_bookmarks = db.Column(db.Integer)

    # bookmark relationship
    bookmarks = db.relationship('Bookmark', backref='library', lazy='dynamic')

    def __init__(self, name, user_id, num_bookmarks):
        self.name = name
        self.user_id = user_id
        self.num_bookmarks = num_bookmarks

    def __repr__(self):
        return '<Library %r>' % self.name


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    description = db.Column(db.Text(256))
    text = db.Column(db.Text())
    image = db.Column(db.Text(256))
    tags = db.Column(db.String(256))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    source = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True) # slug should be unique
    created_at = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # category relationship
    category = db.relationship('Category', backref=db.backref('bookmark', lazy='dynamic'))

    def __init__(self, library, user, category, slug, url, title, source, description=None, image=None, text=None, tags=None):
        self.library_id = library.id
        self.user_id = user.id
        self.url = url
        self.title = title
        self.description = description
        self.image = image
        self.tags = tags
        self.likes = 0
        self.dislikes = 0
        self.source = source
        self.slug = slug
        self.created_at = datetime.utcnow()
        self.category_id = category.id

    def __repr__(self):
        return '<Bookmark %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
