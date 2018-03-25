from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from bookmark.form import ScrapeForm
from flask_newsmarkr import db
from user.models import User
from bookmark.models import Library, Bookmark, Category

# import custom decorators
from user.decorators import login_required

# import bcrypt for password hashing
import bcrypt

# import python-slugify for slug generation
from slugify import slugify

# import scrape helper function
from bookmark.scrape import article_meta_scrape


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    form = ScrapeForm()

    if form.validate_on_submit():
        flash(form.url.data)

    return render_template('bookmark/library.html', form=form)


@app.route('/scrape', methods=['Get', 'POST'])
def scrape():
    form = ScrapeForm()
    error = None
    current_user = User.query.filter_by(username=session['username']).first()
    url_to_scrape = None
    bookmark = None
    meta = None

    if form.validate_on_submit() and current_user:
        url_to_scrape = form.url.data
        meta = article_meta_scrape(current_user, url_to_scrape)

    if meta:
        # set up temp category for bookmark
        new_category = Category('temp')
        db.session.add(new_category)
        db.session.flush()
        category = new_category

        # get library
        library = Library.query.filter_by(user_id=current_user.id).first()

        if library:
            # add bookmark to db
            title = meta['title']
            # description = meta['description']
            description = 'this is a test'
            url = meta['url']
            image = meta['image']
            slug = slugify(title)

            bookmark = Bookmark(library, current_user, category, slug, url, title, description, image, None, None, 0, 0, None)
            db.session.add(bookmark)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('library'))

    return 'no'
