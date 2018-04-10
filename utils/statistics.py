from flask_newsmarkr import db
from bookmark.models import Collection, Bookmark, Category
from social.models import Post, Comment
from profile.models import Friends

# for profile 'about' section statistics
def total_num_posts(userId):
    return Post.query.filter_by(user_id=userId).count()

def total_num_comments(userId):
    return Comment.query.filter_by(user_id=userId).count()

def total_num_friends(userId):
    return Friends.query.filter_by(user_id=userId).count()

def total_num_collections(userId):
    return Collection.query.filter_by(user_id=userId).count()

def total_num_bookmarks_not_posts(userId):
    num_posts = total_num_posts(userId)
    return Bookmark.query.filter_by(user_id=userId).count() - num_posts
