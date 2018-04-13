from flask_newsmarkr import db
from datetime import datetime

class Collection(db.Model):
    """ Model for collection of bookmarks """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80))
    image = db.Column(db.Text(256))
    image_upload = db.Column(db.Text(256))
    category = db.Column(db.String(80))
    num_bookmarks = db.Column(db.Integer)

    # bookmark relationship
    bookmarks = db.relationship('Bookmark', backref='collection', lazy='dynamic')

    def __init__(self, name, user_id, num_bookmarks, image, image_upload, category):
        self.name = name
        self.user_id = user_id
        self.num_bookmarks = num_bookmarks
        self.image = image
        self.image_upload = image_upload
        self.category = category

    def __repr__(self):
        return '<Library %r>' % self.name


class Bookmark(db.Model):
    """ Model for bookmark """
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    description = db.Column(db.Text(256))
    text = db.Column(db.Text())
    image = db.Column(db.Text(256))
    tags = db.Column(db.String(256))
    published_on = db.Column(db.String(256))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    source = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True) # slug should be unique
    created_at = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # category relationship
    category = db.relationship('Category', backref=db.backref('bookmark', lazy='dynamic'))

    def __init__(self, collection, user, category, slug, url, title, source, published_on, description=None, image=None, text=None, tags=None):
        self.collection_id = collection.id
        self.user_id = user.id
        self.url = url
        self.title = title
        self.description = description
        self.image = image
        self.tags = tags
        self.published_on = published_on
        self.likes = 0
        self.dislikes = 0
        self.source = source
        self.slug = slug
        self.created_at = datetime.utcnow()
        self.category_id = category.id

    def __repr__(self):
        return '<Bookmark %r>' % self.title


class Category(db.Model):
    """ Model for bookmark category """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
