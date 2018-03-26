from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from bookmark.form import ScrapeForm
from flask_newsmarkr import db
from user.models import User
from bookmark.models import Library, Bookmark, Category

# import custom decorators
from user.decorators import login_required

# import python-slugify for slug generation
from slugify import slugify

# import scrape helper function
from utils.scrape import article_meta_scrape, bbc_article_content_scrape


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    form = ScrapeForm()

    error = None

    # get all bookmarks in library
    current_user = User.query.filter_by(username=session['username']).first()
    library = Library.query.filter_by(user_id=current_user.id).first()
    if current_user and library:
        bookmarks = Bookmark.query.filter_by(library_id=library.id)
    else:
        error = 'No bookmarks currently found in your library...'

    return render_template('bookmark/library.html', form=form, bookmarks=bookmarks, error=error)

@app.route('/scrape', methods=['POST'])
@app.route('/library/scrape', methods=['POST'])
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
            description = meta['description']
            # description = 'this is a test'
            url = meta['url']
            image = meta['image']
            source = meta['source']
            slug = slugify(title)

            bookmark = Bookmark(library, current_user, category, slug, url, title, source, description, image, None, None)
            db.session.add(bookmark)
            db.session.commit()
            return redirect(url_for('library'))
        else:
            error = 'Please try a different URL...'
    else:
        error = 'Please try a different URL...'

    current_user = User.query.filter_by(username=session['username']).first()
    library = Library.query.filter_by(user_id=current_user.id).first()
    if current_user and library:
        bookmarks = Bookmark.query.filter_by(library_id=library.id)

    return render_template('bookmark/library.html', form=form, bookmarks=bookmarks, error=error)


@app.route('/library/<bookmarkId>', methods=['GET','POST'])
def show_bookmark(bookmarkId):

    bookmark = Bookmark.query.filter_by(id=bookmarkId).first()

    display = bbc_article_content_scrape(bookmark.url)

    return render_template('bookmark/view.html', bookmark_title=bookmark.title, article=display)

@app.route('/library/<bookmarkId>/like', methods=['POST'])
def increment_like(bookmarkId):
    bookmark = Bookmark.query.filter_by(id=bookmarkId).first()
    bookmark.likes += 1
    db.session.commit()
    return redirect(url_for('library'))

@app.route('/library/<bookmarkId>/dislike', methods=['POST'])
def increment_dislike(bookmarkId):
    bookmark = Bookmark.query.filter_by(id=bookmarkId).first()
    bookmark.dislikes += 1
    db.session.commit()
    return redirect(url_for('library'))
