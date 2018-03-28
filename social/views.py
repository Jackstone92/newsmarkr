from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

# import python-slugify for slug generation
from slugify import slugify

from datetime import datetime


from flask_newsmarkr import db

from user.models import User
from bookmark.models import Collection, Bookmark, Category
from social.models import Post, Comment

from social.form import PostForm, CommentForm

# import scrape helper function
from utils.scrape import article_meta_scrape, bbc_article_content_scrape



@app.route('/social-feed', methods=['GET', 'POST'])
def social():
    current_user = User.query.filter_by(username=session['username']).first()
    form = PostForm()
    comment_form = CommentForm()

    posts = Post.query.filter_by(user_id=current_user.id)
    articles = Bookmark.query.filter_by(user_id=current_user.id)

    return render_template('social/social.html', form=form, comment_form=comment_form, posts=posts, articles=articles, current_user=current_user, User=User, Comment=Comment)

@app.route('/social-feed/post', methods=['POST'])
def social_post():
    form = PostForm()
    bookmark = None
    current_user = User.query.filter_by(username=session['username']).first()

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
                if Collection.query.filter_by(name='Posts').first():
                    collection = Collection.query.filter_by(name='Posts').first()
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
                    # TODO: implement proper categories
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
def comment(postId):
    current_user = User.query.filter_by(username=session['username']).first()
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

    return redirect(url_for('social'))


@app.route('/social-feed/<postId>/like', methods=['POST'])
def increment_post_like(postId):
    """ Social-Feed Post method to increment number of likes """
    post = Post.query.filter_by(id=postId).first()
    post.num_likes += 1
    db.session.commit()
    return redirect(url_for('social'))


@app.route('/social-feed/<postId>/dislike', methods=['POST'])
def increment_post_dislike(postId):
    """ Social-Feed Post method to increment number of dislikes """
    post = Post.query.filter_by(id=postId).first()
    post.num_dislikes += 1
    db.session.commit()
    return redirect(url_for('social'))
