from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from datetime import datetime

from flask_newsmarkr import db

from social.models import Post, Comment
from social.form import CommentForm
from profile.models import Friends, FriendRequest
from profile.form import AddFriendsForm
from user.models import User


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/timeline', methods=['GET', 'POST'])
def profile():
    # timeline view
    current_user = User.query.filter_by(username=session['username']).first()

    friends = Friends.query.filter_by(user_id=current_user.id)
    friends_posts = []
    for friend in friends:
        friends_posts.append(Post.query.filter_by(user_id=friend.friend_id))

    posts = Post.query.filter_by(user_id=current_user.id).order_by('id desc')
    comment_form = CommentForm()

    return render_template('profile/profile.html', comment_form=comment_form, posts=posts, Comment=Comment, User=User, current_user=current_user, Friends=Friends)


@app.route('/profile/friends', methods=['GET', 'POST'])
def friends():
    add_friends_form = AddFriendsForm()
    current_user = User.query.filter_by(username=session['username']).first()
    friends = Friends.query.filter_by(user_id=current_user.id)
    pending_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=True, friend_accepted=False)
    friend_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=False)

    return render_template('profile/friends.html', add_friends_form=add_friends_form, friends=friends,friend_requests=friend_requests, pending_requests=pending_requests, User=User)


@app.route('/profile/friends/add-friend', methods=['POST'])
def add_friend():
    add_friends_form = AddFriendsForm()
    current_user = User.query.filter_by(username=session['username']).first()

    if add_friends_form.validate_on_submit():
        username = add_friends_form.username.data
        # check if username is valid
        if User.query.filter_by(username=username).first():
            friend = User.query.filter_by(username=username).first()

            request = FriendRequest(
                current_user.id,
                friend.id,
                True,
                False,
                False,
                False,
                datetime.utcnow(),
                None
            )

            db.session.add(request)
            db.session.flush()

            request2 = FriendRequest(
                friend.id,
                current_user.id,
                False,
                True,
                False,
                False,
                datetime.utcnow(),
                None
            )

            db.session.add(request2)
            db.session.commit()

    return redirect(url_for('friends'))



@app.route('/profile/friends/accept-friend', methods=['POST'])
def accept_friend():
    return redirect(url_for('friends'))


@app.route('/profile/friends/ignore-friend', methods=['POST'])
def ignore_friend():
    return redirect(url_for('friends'))

@app.route('/profile/friends/cancel/<requestId>', methods=['POST'])
def cancel_request(requestId):
    return redirect(url_for('friends'))
