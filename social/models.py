from flask_newsmarkr import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))
    url = db.Column(db.String(256))
    post = db.Column(db.Text())
    posted_on = db.Column(db.Date)
    num_comments = db.Column(db.Integer)
    num_likes = db.Column(db.Integer)
    num_dislikes = db.Column(db.Integer)

    def __init__(self, user_id, collection_id, bookmark_id, url, post, posted_on, num_comments, num_likes, num_dislikes):
        self.user_id = user_id
        self.collection_id = collection_id
        self.bookmark_id = bookmark_id
        self.url = url
        self.post = post
        self.posted_on = posted_on
        self.num_comments = num_comments
        self.num_likes = num_likes
        self.num_dislikes = num_dislikes

    def __repr__(self):
        return '<Post %r>' % self.post


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
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
