from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

# import python-slugify for slug generation
from slugify import slugify

from datetime import datetime


from flask_newsmarkr import db

from user.models import User
from bookmark.models import Collection, Bookmark, Category
from social.models import Post, Comment

from social.form import PostForm

# import scrape helper function
from utils.scrape import article_meta_scrape, bbc_article_content_scrape



@app.route('/social-feed', methods=['GET', 'POST'])
def social():
    form = PostForm()

    return render_template('social/social.html', form=form)

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
            # if it isn't, create new bookmark
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
                        'https://dummyimage.com/1920x1280/000/fff&text=Insert+Image',
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
                form_post,
                datetime.utcnow(),
                0,
                0,
                0
            )
            db.session.add(post)
            db.session.commit()

    return redirect(url_for('social'))
