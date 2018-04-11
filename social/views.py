from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from flask_login import login_required, current_user

# import python-slugify for slug generation
from slugify import slugify

from datetime import datetime


from flask_newsmarkr import db

from user.models import User
from bookmark.models import Collection, Bookmark, Category
from social.models import Post, Comment
from profile.models import Friends

from social.form import PostForm, CommentForm

# import scrape helper function
from utils.scrape import article_meta_scrape, bbc_article_content_scrape


@app.route('/social-feed', methods=['GET', 'POST'])
@login_required
def social():
    form = PostForm()
    comment_form = CommentForm()
    share_url = None
    friends_posts = []
    both = []
    combined_posts = []

    if request.args.get('share_url'):
        share_url = request.args.get('share_url')

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

    articles = Bookmark.query.filter_by(user_id=current_user.id)

    return render_template('social/social.html', share_url=share_url, form=form, comment_form=comment_form, posts=combined_posts, articles=articles, current_user=current_user, User=User, Comment=Comment)


@app.route('/social-feed/<postId>', methods=['GET', 'POST'])
@login_required
def show_social_article(postId):
    """ Social-Feed display page """
    comment_form = CommentForm()
    post = Post.query.filter_by(id=postId).first()
    article = None

    # determine which scraping tools to use
    if post.source == 'BBC News':
        article = bbc_article_content_scrape(post.url)
    elif post.source == 'Sky News':
        article = '<h1>NOpe</h1>'
    else:
        article = '<h1>NOpe</h1>'

    return render_template('social/view.html', comment_form=comment_form, post=post, article_title=post.title, article=article, current_user=current_user, User=User, Comment=Comment)


@app.route('/social-feed/post', methods=['POST'])
@login_required
def social_post():
    form = PostForm()
    bookmark = None

    if form.validate_on_submit():
        form_url = form.url.data
        form_post = form.post.data

        # check if article is already a bookmark
        if Bookmark.query.filter_by(url=form_url).first():
            # if it is, grab relevant info to add to post
            bookmark = Bookmark.query.filter_by(url=form_url).first()
        else:
            # if it isn't, create new PostArticle
            url_to_scrape = form_url
            meta = article_meta_scrape(current_user, url_to_scrape)

            if meta:
                # find or create 'Posts' collection
                if Collection.query.filter_by(user_id=current_user.id, name='Posts').first():
                    collection = Collection.query.filter_by(user_id=current_user.id, name='Posts').first()
                else:
                    collection = Collection(
                        'Posts',
                        current_user.id,
                        0,
                        'https://dummyimage.com/1920x1280/000/fff&text=Posts',
                        '',
                        'Posts'
                    )
                    db.session.add(collection)
                    db.session.flush()

                if collection:
                    collection.num_bookmarks += 1
                    db.session.flush()

                    # add bookmark to db
                    title = meta['title']
                    description = meta['description']
                    # description = 'this is a test'
                    url = meta['url']
                    image = meta['image']
                    source = meta['source']
                    slug = slugify(title)
                    published_on = datetime.utcnow()
                    if Category.query.filter_by(name='Posts').first():
                        category = Category.query.filter_by(name='Posts').first()
                    else:
                        category = Category(
                            'Posts'
                        )
                        db.session.add(category)
                        db.session.flush()

                    bookmark = Bookmark(
                        collection,
                        current_user,
                        category,
                        slug,
                        url,
                        title,
                        source,
                        published_on,
                        description,
                        image,
                        None,
                        None
                    )
                    db.session.add(bookmark)
                    db.session.flush()

        # create post
        if bookmark:
            post = Post(
                current_user.id,
                bookmark.collection_id,
                bookmark.id,
                form_url,
                bookmark.title,
                bookmark.description,
                bookmark.text,
                bookmark.image,
                bookmark.tags,
                bookmark.published_on,
                bookmark.source,
                form_post,
                datetime.utcnow(),
                0,
                0,
                0
            )
            db.session.add(post)
            db.session.commit()

    return redirect(url_for('social'))


@app.route('/social-feed/<postId>/comment', methods=['POST'])
@login_required
def comment(postId):
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        form_comment = comment_form.comment.data

        comment = Comment(
            postId,
            current_user.id,
            datetime.utcnow(),
            form_comment
        )

        db.session.add(comment)
        db.session.flush()

        # increment num_comments
        post = Post.query.filter_by(id=postId).first()
        post.num_comments += 1

        db.session.commit()

        if request.args.get('current_page') == 'View':
            return redirect(url_for('show_social_article', postId=postId))

    return redirect(url_for('social'))


@app.route('/social-feed/<postId>/like', methods=['POST'])
@login_required
def increment_post_like(postId):
    """ Social-Feed Post method to increment number of likes """
    post = Post.query.filter_by(id=postId).first()
    post.num_likes += 1
    db.session.commit()
    return redirect(url_for('social'))


@app.route('/social-feed/<postId>/dislike', methods=['POST'])
@login_required
def increment_post_dislike(postId):
    """ Social-Feed Post method to increment number of dislikes """
    post = Post.query.filter_by(id=postId).first()
    post.num_dislikes += 1
    db.session.commit()
    return redirect(url_for('social'))
