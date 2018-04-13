from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from flask_login import login_required, current_user

import os
from settings import UPLOADED_IMAGES_DEST

from datetime import datetime
# geocoder for ip location detection
import geocoder

from flask_newsmarkr import db, uploaded_images

from social.models import Post, Comment
from social.form import CommentForm
from profile.models import Friends, FriendRequest, Profile
# constants from profile selection
from profile.models import POLITICAL_SPECTRUM, POLITICAL_PARTIES, FAVOURITE_NEWS_WEBSITES, NEWS_WEBSITE_LINKS
from profile.form import AddFriendsForm, EditProfilePicture, EditCoverPhoto, EditAbout
from user.models import User

# functions for obtaining profile stats
from utils.statistics import total_num_posts, total_num_comments, total_num_friends, total_num_collections, total_num_bookmarks_not_posts


# ============================================================== #
#                                                                #
#                          Timeline                              #
#                                                                #
# ============================================================== #
@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/timeline', methods=['GET', 'POST'])
@login_required
def profile():
    """ Displays profile timeline view """
    # timeline view
    comment_form = CommentForm()
    friends_posts = []
    both = []
    combined_posts = []

    # if 'my posts' selected
    if request.args.get('posts') == 'Just My Posts':
        # posts by current_user only
        posts = Post.query.filter_by(user_id=current_user.id).order_by('id desc')

        return render_template('profile/my-posts.html', comment_form=comment_form, current_user=current_user, posts=posts, User=User, Comment=Comment)

    else:
        # else display 'my posts' and friends' posts
        posts = Post.query.filter_by(user_id=current_user.id).order_by('id desc')
        for friend in Friends.query.filter_by(friend_id=current_user.id):
            for post in Post.query.filter_by(user_id=friend.user_id).order_by('id desc'):
                friends_posts.append(post)

        # list comprehension to combine current_user posts and friends_posts posts
        if posts and friends_posts:
            both.append(posts)
            both.append(friends_posts)
            combined_posts = [item for sublist in both for item in sublist]
            combined_posts = sorted(combined_posts, key=lambda post: post.id, reverse=True)
        else:
            combined_posts = [item for item in posts]

        return render_template('profile/timeline.html', comment_form=comment_form, posts=combined_posts, Comment=Comment, User=User, current_user=current_user, Friends=Friends)



# ============================================================== #
#                                                                #
#                            About                               #
#                                                                #
# ============================================================== #
@app.route('/profile/about', methods=['GET', 'POST'])
@login_required
def about():
    """ Displays profile about view """
    # about view
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    display_profile = {}
    # get profile content from constants to render in template
    if profile:
        display_profile['birthday'] = profile.birthday
        display_profile['political_spectrum'] = POLITICAL_SPECTRUM[profile.political_spectrum]
        display_profile['political_party'] = POLITICAL_PARTIES[profile.political_party]
        display_profile['favourite_news_websites'] = profile.favourite_news_websites.split(',')
        display_profile['allow_location_detection'] = str(profile.allow_location_detection)
        display_profile['location'] = profile.location
        display_profile['lat'] = profile.lat
        display_profile['lon'] = profile.lon

    # get stats
    statistics = {}
    statistics['total_num_posts'] = total_num_posts(current_user.id)
    statistics['total_num_comments'] = total_num_comments(current_user.id)
    statistics['total_num_friends'] = total_num_friends(current_user.id)
    statistics['total_num_collections'] = total_num_collections(current_user.id)
    statistics['total_num_bookmarks_not_posts'] = total_num_bookmarks_not_posts(current_user.id)

    return render_template('profile/about.html', current_user=current_user, profile=display_profile, statistics=statistics, FAVOURITE_NEWS_WEBSITES=FAVOURITE_NEWS_WEBSITES, NEWS_WEBSITE_LINKS=NEWS_WEBSITE_LINKS)



# ============================================================== #
#                                                                #
#                           Friends                              #
#                                                                #
# ============================================================== #
@app.route('/profile/friends', methods=['GET', 'POST'])
@login_required
def friends():
    """ Displays profile friends view """
    # friends view
    add_friends_form = AddFriendsForm()
    friends = Friends.query.filter_by(user_id=current_user.id)
    pending_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=True, friend_accepted=False, user_ignored=False, friend_ignored=False)
    friend_requests = FriendRequest.query.filter_by(user_id=current_user.id, user_accepted=False, friend_accepted=True, user_ignored=False, friend_ignored=False)

    edit_status_friends = None
    if 'edit_status_friends' in session:
        edit_status_friends = session['edit_status_friends']
    else:
        session['edit_status_friends'] = False
        edit_status_friends = session['edit_status_friends']

    return render_template('profile/friends.html', add_friends_form=add_friends_form, friends=friends,friend_requests=friend_requests, pending_requests=pending_requests, User=User, current_user=current_user, edit_status_friends=edit_status_friends)


@app.route('/profile/friends/add-friend', methods=['POST'])
@login_required
def add_friend():
    """ Profile post method to make friend request """
    add_friends_form = AddFriendsForm()

    if add_friends_form.validate_on_submit():
        username = add_friends_form.username.data
        # check if username is valid
        if User.query.filter_by(username=username).first():
            friend = User.query.filter_by(username=username).first()
            # check if already friend
            if not Friends.query.filter_by(user_id=current_user.id, friend_id=friend.id).first() and not Friends.query.filter_by(user_id=friend.id, friend_id=current_user.id).first():
                # check request has not already been made
                if not FriendRequest.query.filter_by(user_id=current_user.id, friend_id=friend.id).first() and not FriendRequest.query.filter_by(user_id=friend.id, friend_id=current_user.id).first():
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


@app.route('/profile/friends/accept-friend/<userId>/<friendId>', methods=['POST'])
@login_required
def accept_friend(userId, friendId):
    """ Profile post method to accept friend request """
    request = FriendRequest.query.filter_by(user_id=userId, friend_id=friendId).first()
    request2 = FriendRequest.query.filter_by(user_id=friendId, friend_id=userId).first()

    if request and request2:
        request.user_accepted = True
        request.friend_accepted = True
        request.accepted_on = datetime.utcnow()
        request2.user_accepted = True
        request2.friend_accepted = True
        request2.accepted_on = datetime.utcnow()

        db.session.flush()

        friend_acceptance = Friends(
            userId,
            friendId,
            request.created_on,
            datetime.utcnow()
        )

        friend_acceptance2 = Friends(
            friendId,
            userId,
            request.created_on,
            datetime.utcnow()
        )

        db.session.add(friend_acceptance)
        db.session.add(friend_acceptance2)
        db.session.commit()

    return redirect(url_for('friends'))


@app.route('/profile/friends/ignore-friend/<userId>/<friendId>', methods=['POST'])
@login_required
def ignore_friend(userId, friendId):
    """ Profile post method to ignore a friend request """
    request = FriendRequest.query.filter_by(user_id=userId, friend_id=friendId).first()
    request2 = FriendRequest.query.filter_by(user_id=friendId, friend_id=userId).first()

    if request.user_ignored == False and request2.friend_ignored == False:
        request.user_ignored = True
        request2.friend_ignored = True

        db.session.commit()

    return redirect(url_for('friends'))

@app.route('/profile/friends/cancel/<userId>/<friendId>', methods=['POST'])
@login_required
def cancel_request(userId, friendId):
    """ Profile post method to cancel a friend request """
    request = FriendRequest.query.filter_by(user_id=userId, friend_id=friendId)
    request2 = FriendRequest.query.filter_by(user_id=friendId, friend_id=userId)

    for req in request:
        db.session.delete(req)

    db.session.flush()

    for request in request2:
        db.session.delete(request)

    db.session.commit()

    return redirect(url_for('friends'))


@app.route('/profile/friends/change-edit-status', methods=['POST'])
@login_required
def change_edit_status_friends():
    """ Profile post method to change friend request status """
    if 'edit_status_friends' in session:
        edit_status_friends = session['edit_status_friends']
        session['edit_status_friends'] = not edit_status_friends
    else:
        session['edit_status_friends'] = False

    return redirect(url_for('friends'))


@app.route('/profile/friends/delete-friend/<userId>/<friendId>', methods=['POST'])
@login_required
def delete_friend(userId, friendId):
    """ Profile post method to delete friend """
    # remove original request
    request = FriendRequest.query.filter_by(user_id=userId, friend_id=friendId)
    request2 = FriendRequest.query.filter_by(user_id=friendId, friend_id=userId)

    for req in request:
        db.session.delete(req)

    db.session.flush()

    for request in request2:
        db.session.delete(request)

    db.session.flush()

    # delete friend
    friend_to_remove = Friends.query.filter_by(user_id=userId, friend_id=friendId)
    friend_to_remove2 = Friends.query.filter_by(user_id=friendId, friend_id=userId)

    for req in friend_to_remove:
        db.session.delete(req)

    db.session.flush()

    for req in friend_to_remove2:
        db.session.delete(req)

    db.session.commit()

    return redirect(url_for('friends'))



# ============================================================== #
#                                                                #
#                         Edit Profile                           #
#                                                                #
# ============================================================== #
@app.route('/profile/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Displays edit profile view """
    # edit profile view
    edit_cover_photo_form = EditCoverPhoto()
    edit_profile_picture_form = EditProfilePicture()
    edit_about_form = EditAbout()
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    # set edit_about_form values
    if profile:
        edit_about_form.birthday.data = profile.birthday
        edit_about_form.political_spectrum.data = profile.political_spectrum
        edit_about_form.political_party.data = profile.political_party
        edit_about_form.favourite_news_websites.data = profile.favourite_news_websites.split(',')
        # convert db bool to 'yes' or 'no'
        edit_about_form.allow_location_detection.data = 'yes' if profile.allow_location_detection == True else 'no'

    return render_template('profile/edit-profile.html', current_user=current_user, profile=profile, edit_cover_photo_form=edit_cover_photo_form, edit_profile_picture_form=edit_profile_picture_form, edit_about_form=edit_about_form)


@app.route('/profile/edit-profile/edit-profile-picture', methods=['POST'])
@login_required
def edit_profile_picture():
    """ Profile post method to edit profile picture """
    edit_profile_picture_form = EditProfilePicture()

    if edit_profile_picture_form.validate_on_submit():
        filename = None
        profile_picture = edit_profile_picture_form.profile_picture.data
        profile_picture_upload = edit_profile_picture_form.profile_picture_upload.data

        try:
            filename = uploaded_images.save(profile_picture_upload)
        except:
            flash('The image was not uploaded')

        if profile_picture or profile_picture_upload:
            # if image, use that rather than filename
            if profile_picture and current_user.profile_picture != profile_picture:
                current_user.profile_picture_upload = None
                current_user.profile_picture = profile_picture

            # if filename, use that rather than image
            if filename and current_user.profile_picture_upload != filename:
                current_user.profile_picture = None
                current_user.profile_picture_upload = filename

            db.session.commit()

    return redirect(url_for('edit_profile'))


@app.route('/profile/edit-profile/edit-cover-photo', methods=['POST'])
@login_required
def edit_cover_photo():
    """ Profile post method to edit cover photo """
    edit_cover_photo_form = EditCoverPhoto()

    if edit_cover_photo_form.validate_on_submit():
        filename = None
        cover_photo = edit_cover_photo_form.cover_photo.data
        cover_photo_upload = edit_cover_photo_form.cover_photo_upload.data

        try:
            filename = uploaded_images.save(cover_photo_upload)
        except:
            flash('The image was not uploaded')

        if cover_photo or cover_photo_upload:
            # if image, use that rather than filename
            if cover_photo and current_user.cover_photo != cover_photo:
                current_user.cover_photo_upload = None
                current_user.cover_photo = cover_photo

            # if filename, use that rather than image
            if filename and current_user.cover_photo_upload != filename:
                current_user.cover_photo = None
                current_user.cover_photo_upload = filename

            db.session.commit()

    return redirect(url_for('edit_profile'))


@app.route('/profile/edit-profile/edit-about/<userId>', methods=['POST'])
@login_required
def edit_about(userId):
    """ Profile post method to edit about """
    edit_about_form = EditAbout()

    if edit_about_form.validate_on_submit():
        birthday = edit_about_form.birthday.data
        political_spectrum = edit_about_form.political_spectrum.data
        political_party = edit_about_form.political_party.data
        favourite_news_websites = edit_about_form.favourite_news_websites.data
        allow_location_detection = edit_about_form.allow_location_detection.data

        profile = Profile.query.filter_by(user_id=userId).first()
        if profile:
            # update profile
            if profile.birthday != birthday:
                profile.birthday = birthday
                db.session.flush()

            if profile.political_spectrum != political_spectrum:
                profile.political_spectrum = political_spectrum
                db.session.flush()

            if profile.political_party != political_party:
                profile.political_party = political_party
                db.session.flush()

            if profile.favourite_news_websites != ",".join(favourite_news_websites):
                profile.favourite_news_websites = ",".join(favourite_news_websites)
                db.session.flush()

            if profile.allow_location_detection == True and allow_location_detection == 'no' or profile.allow_location_detection == False and allow_location_detection == 'yes':
                if allow_location_detection == 'yes':
                    profile.allow_location_detection = True
                else:
                    profile.allow_location_detection = False

                db.session.flush()
        else:
            # create new profile
            # convert allow_location_detection to bool
            allow_bool = None
            if allow_location_detection == 'yes':
                allow_bool = True
            else:
                allow_bool = False

            profile = Profile(
                userId,
                birthday,
                political_spectrum,
                political_party,
                favourite_news_websites,
                allow_bool,
                None,
                None,
                None
            )
            db.session.add(profile)
            db.session.flush()

        # if allow_location_detection, get location
        if profile.allow_location_detection == True:
            g = geocoder.ip('me')
            if profile.location != g.city + ", " + g.country or profile.lat != g.latlng[0] or profile.lon != g.latlng[1]:
                # add location
                profile.lat = g.latlng[0]
                profile.lon = g.latlng[1]
                profile.location = g.city + ", " + g.country
                db.session.flush()

        db.session.commit()

    return redirect(url_for('about'))
