from flask_newsmarkr import db
from datetime import datetime

class ArticlePool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    slug = db.Column(db.String(256)) # slug should be unique

    live_comment = db.relationship('LiveComment', backref='article_pool', lazy='dynamic')

    def __init__(self, url, title, description, text, image, tags, published_on, likes, dislikes, source, slug):
        self.url = url
        self.title = title
        self.description = description
        self.text = text
        self.image = image
        self.tags = tags
        self.published_on = published_on
        self.likes = likes
        self.dislikes = dislikes
        self.source = source
        self.slug = slug

    def __repr__(self):
        return '<ArticlePool %r>' % self.title


class LiveComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_pool_id = db.Column(db.Integer, db.ForeignKey('article_pool.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted_on = db.Column(db.Date)
    comment = db.Column(db.Text())

    def __init__(self, post_id, user_id, posted_on, comment):
        self.post_id = post_id
        self.user_id = user_id
        self.posted_on = posted_on
        self.comment = comment

    def __repr__(self):
        return '<Comment %r>' % self.comment
