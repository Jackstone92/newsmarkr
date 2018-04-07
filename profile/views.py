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
    pending_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=True, friend_accepted=False, user_ignored=False, friend_ignored=False)
    friend_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=False, friend_accepted=True, user_ignored=False, friend_ignored=False)

    return render_template('profile/friends.html', add_friends_form=add_friends_form, friends=friends,friend_requests=friend_requests, pending_requests=pending_requests, User=User, current_user=current_user)


@app.route('/profile/friends/add-friend', methods=['POST'])
def add_friend():
    add_friends_form = AddFriendsForm()
    current_user = User.query.filter_by(username=session['username']).first()

    if add_friends_form.validate_on_submit():
        username = add_friends_form.username.data
        # check if username is valid
        if User.query.filter_by(username=username).first():
            friend = User.query.filter_by(username=username).first()
            if not Friends.query.filter_by(user_id=current_user.id, friend_id=friend.id).first() or Friends.query.filter_by(user_id=friend.id, friend_id=current_user.id).first():
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


@app.route('/profile/friends/accept-friend/<userId>', methods=['GET', 'POST'])
def accept_friend(userId):
    request = FriendRequest.query.filter_by(user_id=userId).first()
    request2 = FriendRequest.query.filter_by(friend_id=userId).first()

    if request and request2:
        friend_id = request.friend_id

        request.user_accepted = True
        request.friend_accepted = True
        request2.user_accepted = True
        request2.friend_accepted = True

        db.session.flush()

        friend_acceptance = Friends(
            userId,
            friend_id,
            request.created_on,
            datetime.utcnow()
        )

        db.session.add(friend_acceptance)
        db.session.flush()

        friend_acceptance2 = Friends(
            friend_id,
            userId,
            request.created_on,
            datetime.utcnow()
        )

        db.session.add(friend_acceptance2)
        db.session.commit()

    return redirect(url_for('friends'))


@app.route('/profile/friends/ignore-friend/<userId>', methods=['GET', 'POST'])
def ignore_friend(userId):
    request = FriendRequest.query.filter_by(user_id=userId).first()
    request2 = FriendRequest.query.filter_by(friend_id=userId).first()

    request.user_ignored = True
    request2.friend_ignored = True

    db.session.commit()

    return redirect(url_for('friends'))

@app.route('/profile/friends/cancel/<userId>', methods=['GET', 'POST'])
def cancel_request(userId):
    request = FriendRequest.query.filter_by(user_id=userId).first()
    request2 = FriendRequest.query.filter_by(friend_id=userId).first()

    db.session.delete(request)
    db.session.delete(request2)
    db.session.commit()

    return redirect(url_for('friends'))


@app.route('/profile/friends/delete-friend/<friendId>', methods=['GET', 'POST'])
def delete_friend(friendId):
    current_user = User.query.filter_by(username=session['username']).first()

    friend_to_remove = Friends.query.filter_by(user_id=current_user.id, friend_id=friendId).first()
    friend_to_remove2 = Friends.query.filter_by(user_id=friendId, friend_id=current_user.id).first()

    db.session.delete(friend_to_remove)
    db.session.delete(friend_to_remove2)
    db.session.commit()

    return redirect(url_for('friends'))



@app.route('/profile/my-shares', methods=['GET', 'POST'])
def my_shares():
    current_user = User.query.filter_by(username=session['username']).first()

    return render_template('profile/my-shares.html', current_user=current_user)
#
