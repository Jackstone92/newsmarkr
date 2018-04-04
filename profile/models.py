from flask_newsmarkr import db
from datetime import datetime

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.Date)
    accepted_on = db.Column(db.Date)

    def __init__(self, user_id, friend_id, created_on, accepted_on):
        self.user_id = user_id
        self.friend_id = friend_id
        self.created_on = created_on
        self.accepted_on = accepted_on

    def __repr__(self):
        return '<Friends %r>' % self.user_id


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_accepted = db.Column(db.Boolean)
    friend_accepted = db.Column(db.Boolean)
    user_ignored = db.Column(db.Boolean)
    friend_ignored = db.Column(db.Boolean)
    created_on = db.Column(db.Date)
    accepted_on = db.Column(db.Date)

    def __init__(self, user_id, friend_id, user_accepted, friend_accepted, user_ignored, friend_ignored, created_on, accepted_on):
        self.user_id = user_id
        self.friend_id = friend_id
        self.user_accepted = user_accepted
        self.friend_accepted = friend_accepted
        self.user_ignored = user_ignored
        self.friend_ignored = friend_ignored
        self.created_on = created_on
        self.accepted_on = accepted_on

    def __repr__(self):
        return '<FriendRequest %r>' % self.user_id
