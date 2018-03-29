from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

# feedparser for parsing rss feeds
import feedparser

from flask_newsmarkr import db
from user.models import User
from bookmark.models import Collection

from utils.scrape import article_meta_scrape, article_content_scrape

# dictionary of rss feed urls
RSS_FEEDS = {
                'bbc': 'http://feeds.bbci.co.uk/news/rss.xml'
                # 'sky_home': 'http://feeds.skynews.com/feeds/rss/home.xml',
                # 'cnn': 'http://rss.cnn.com/rss/edition.rss'
            }

@app.route('/browse-headlines', methods=['GET'])
def browse():
    articles = []

    for key in RSS_FEEDS:
        feed = feedparser.parse(RSS_FEEDS[key])
        for entry in feed['entries']:
            articles.append(entry)

    return render_template('articlepool/browse.html', articles=articles)

@app.route('/browse-headlines/<articleTitle>', methods=['GET'])
def view_browse_article(articleTitle):

    article_title = articleTitle


    return render_template('articlepool/view.html', article_title=articleTitle, article='<h1>Article</h1>')


@app.route('/browse-headlines/<articleTitle>/share', methods=['POST'])
def share_browse_article(articleTitle):
    share_url = None

    if request.args.get('share_url'):
        share_url = request.args.get('share_url')

    return redirect(url_for('social', share_url=share_url))


@app.route('/browse-headlines/<articleTitle>/bookmark', methods=['POST'])
def bookmark_browse_article(articleTitle):
    bookmark_url = None
    collectionId = None

    if request.args.get('bookmark_url'):
        bookmark_url = request.args.get('bookmark_url')

    # if browse collection doesn't exist, create one
    if Collection.query.filter_by(name='Browse').first():
        collectionId = Collection.query.filter_by(name='Browse').first().id
    else:
        current_user = User.query.filter_by(username=session['username']).first()
        collection = Collection(
            'Browse',
            current_user.id,
            0,
            'https://dummyimage.com/1920x1280/000/fff&text=Browse',
            '',
            'Browse'
        )
        db.session.add(collection)
        db.session.commit()

        collectionId = collection.id

    return redirect(url_for('scrape', collectionId=collectionId, bookmark_url=bookmark_url))
