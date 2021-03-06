from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from flask_login import login_required, current_user

# for uploaded file deletion
import os
from settings import UPLOADED_IMAGES_DEST

from datetime import datetime

from bookmark.form import SearchForm, ScrapeForm, EditForm
from flask_newsmarkr import db, uploaded_images
from user.models import User
from bookmark.models import Collection, Bookmark, Category
from social.models import Post

# import python-slugify for slug generation
from slugify import slugify

# import scrape helper function
from utils.scrape import article_meta_scrape, bbc_article_content_scrape

# ============================================================== #
#                                                                #
#                            Index                               #
#                                                                #
# ============================================================== #
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """ Main index page """
    return render_template('index.html')


# ============================================================== #
#                                                                #
#                           Library                              #
#                                                                #
# ============================================================== #
@app.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    """ Library page, displayed after login. Lists all collections and contains search functionality """
    form = SearchForm()
    collections = None
    error = None

    # implement search functionality

    # get all collections
    collections = Collection.query.filter_by(user_id=current_user.id)

    return render_template('bookmark/library.html', form=form, collections=collections, error=error)


@app.route('/library/add', methods=['GET', 'POST'])
@login_required
def add_collection():
    """ Library method to add new collection """
    # create new collection
    collection = Collection(
        'New Collection',
        current_user.id,
        0,
        'https://dummyimage.com/1920x1280/000/fff&text=Insert+Image',
        '',
        'New Category'
    )
    # add to database
    db.session.add(collection)
    # flush and check before committing
    db.session.flush()
    if(collection.id):
        # actually commit
        db.session.commit()
        return redirect(url_for('library'))
    else:
        # undo flush by rollback()
        db.session.rollback()
        error = "Error creating collection"
        flash(error)
        return error



# ============================================================== #
#                                                                #
#                          Collection                            #
#                                                                #
# ============================================================== #
@app.route('/library/<collectionId>', methods=['GET', 'POST'])
@login_required
def collection(collectionId):
    """ Collection page. Lists bookmarks in current collection """
    form = ScrapeForm()
    edit_form = EditForm()
    bookmarks = None
    edit_bookmark_status = None
    if request.args.get('error'):
        error = request.args.get('error')
    else:
        error = None

    # session for edit bookmarks status
    if 'edit_bookmark_status' in session:
        edit_bookmark_status = session['edit_bookmark_status']
    else:
        session['edit_bookmark_status'] = False

    # get all bookmarks in library
    collection = Collection.query.filter_by(id=collectionId).first()
    if current_user and collection:
        bookmarks = Bookmark.query.filter_by(collection_id=collectionId).order_by('id desc')
    else:
        error = 'No collections currently found in your library...'

    return render_template('bookmark/bookmarks.html', form=form, edit_form=edit_form, bookmarks=bookmarks, error=error, collection=collection, edit_bookmark_status=edit_bookmark_status)

@app.route('/library/<collectionId>/change-edit-status', methods=['POST'])
@login_required
def change_edit_status(collectionId):
    """ Collection method to change edit status """
    if 'edit_bookmark_status' in session:
        edit_bookmark_status = session['edit_bookmark_status']
        session['edit_bookmark_status'] = not edit_bookmark_status
    else:
        session['edit_bookmark_status'] = False

    return redirect(url_for('collection', collectionId=collectionId))

@app.route('/library/<collectionId>/edit-collection', methods=['POST'])
@login_required
def edit_collection(collectionId):
    """ Collection method to update collection db """
    edit_form = EditForm()
    name = None
    image = None
    image_upload = None
    category = None

    image = None
    filename = None

    if edit_form.validate_on_submit():
        name = edit_form.name.data
        image = edit_form.image.data
        # handle image upload
        image_upload = edit_form.image_upload.data
        try:
            filename = uploaded_images.save(image_upload)
        except:
            flash('The image was not uploaded')

        category = edit_form.category.data

        if name and image or image_upload and category:
            collection = Collection.query.filter_by(id=collectionId).first()
            if collection.name != name:
                collection.name = name

            # if image, use that rather than filename
            if image and collection.image != image:
                collection.image_upload = ''
                collection.image = image

            # if filename, use that rather than image
            if filename and collection.image_upload != filename:
                collection.image = ''
                collection.image_upload = filename

            if collection.category != category:
                collection.category = category

            db.session.commit()

    return redirect(url_for('collection', collectionId=collectionId))

@app.route('/library/<collectionId>/delete-collection', methods=['GET', 'POST'])
@login_required
def delete_collection(collectionId):
    """ Collection method to delete a collection """
    collection_to_delete = Collection.query.filter_by(id=collectionId).first()
    # delete all bookmarks within collection
    bookmarks_to_delete = Bookmark.query.filter_by(collection_id=collection_to_delete.id)

    # delete collection image_upload images
    if collection_to_delete.image_upload:
        os.remove(os.path.join(UPLOADED_IMAGES_DEST, collection_to_delete.image_upload))

    for bookmark in bookmarks_to_delete:
        db.session.delete(bookmark)

    db.session.flush()
    # delete collection
    db.session.delete(collection_to_delete)
    # commit changes
    db.session.commit()
    # redirect back to library page
    return redirect(url_for('library'))

@app.route('/library/<collectionId>/delete-bookmark', methods=['POST'])
@login_required
def delete_bookmark(collectionId):
    """ Bookmark post method to delete a bookmark """
    # get bookmarkId from request
    bookmarkId = request.args.get('bookmarkId')
    # bookmark that should be deleted
    bookmark_to_delete = Bookmark.query.filter_by(id=bookmarkId).first()
    # delete bookmark
    db.session.delete(bookmark_to_delete)
    db.session.flush()
    # decrement num_bookmarks from collection
    collection = Collection.query.filter_by(id=collectionId).first()
    collection.num_bookmarks -= 1

    db.session.commit()

    return redirect(url_for('collection', collectionId=collectionId))

@app.route('/library/<collectionId>/scrape', methods=['GET', 'POST'])
@login_required
def scrape(collectionId):
    """ Bookmark scrape method """
    form = ScrapeForm()
    if request.args.get('error'):
        error = request.args.get('error')
    else:
        error = None

    if request.args.get('bookmark_url'):
        url_to_scrape = request.args.get('bookmark_url')
        meta = article_meta_scrape(current_user, url_to_scrape)
    elif form.validate_on_submit():
        url_to_scrape = form.url.data
        meta = article_meta_scrape(current_user, url_to_scrape)
    else:
        url_to_scrape = None
        meta = None

    bookmark = None

    if meta:
        # set up temp category for bookmark
        new_category = Category('temp')
        db.session.add(new_category)
        db.session.flush()
        category = new_category

        # get library
        collection = Collection.query.filter_by(id=collectionId).first()

        # increment num_bookmarks for that collection
        collection.num_bookmarks += 1
        db.session.flush()

        if collection:
            # add bookmark to db
            title = meta['title']
            description = meta['description']
            url = meta['url']
            image = meta['image']
            source = meta['source']
            slug = slugify(title)
            published_on = datetime.utcnow()

            bookmark = Bookmark(collection, current_user, category, slug, url, title, source, published_on, description, image, None, None)
            db.session.add(bookmark)
            db.session.commit()
            return redirect(url_for('collection', collectionId=collectionId))
        else:
            error = 'Please try a different URL...'

    else:
        error = 'Please try a different URL...'

    return redirect(url_for('collection', collectionId=collectionId, error=error))



# ============================================================== #
#                                                                #
#                           Bookmark                             #
#                                                                #
# ============================================================== #
@app.route('/library/<collectionId>/<bookmarkId>', methods=['GET','POST'])
@login_required
def show_bookmark(collectionId, bookmarkId):
    """ Bookmark display page. Displays bookmark from within a collection """
    bookmark = Bookmark.query.filter_by(id=bookmarkId).first()
    article = None

    # determine which scraping tools to use
    if bookmark.source == 'BBC News':
        article = bbc_article_content_scrape(bookmark.url)
    elif bookmark.source == 'Sky News':
        article = '<h1>NOpe</h1>'
    else:
        article = '<h1>NOpe</h1>'

    return render_template('bookmark/view.html', bookmark_title=bookmark.title, article=article, collectionId=collectionId)
