from flask_newsmarkr import db
from datetime import datetime

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # bookmark relationship
    bookmarks = db.relationship('Bookmark', backref='library', lazy='dynamic')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<Library %r>' % self.name


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    url = db.Column(db.String(80))
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    text = db.Column(db.String(80))
    image = db.Column(db.String(80))
    tags = db.Column(db.String(80))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    slug = db.Column(db.String(256), unique=True) # slug should be unique
    created_at = db.Column(db.DateTime)
    last_visited_at = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # category relationship
    category = db.relationship('Category', backref=db.backref('bookmark', lazy='dynamic'))

    def __init__(self, library, user, category, url, title, description=None, text=None, image=None, tags=None, likes=0, dislikes=0, slug=None, created_at=None):
        self.library_id = library.id
        self.user_id = user.id
        self.url = url
        self.title = title
        self.description = description
        self.image = image
        self.tags = tags
        self.likes = likes
        self.dislikes = dislikes
        self.slug = slug

        if created_at is None:
            self.created_at = datetime.utcnow()
        else:
            self.create_at = created_at

        if last_visited_at is None:
            self.last_visited_at = datetime.utcnow()
        else:
            self.last_visited_at = last_visited_at

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
