from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

from datetime import datetime

# feedparser for parsing rss feeds
import feedparser

# import python-slugify for slug generation
from slugify import slugify

from flask_newsmarkr import db
from user.models import User
from bookmark.models import Collection, Bookmark
from articlepool.models import ArticlePool, LiveComment
from articlepool.form import LiveCommentForm

from utils.scrape import article_meta_scrape, article_content_scrape, bbc_article_content_scrape

# dictionary of rss feed urls
RSS_FEEDS = {
                'bbc': 'http://feeds.bbci.co.uk/news/rss.xml'
                # 'sky_home': 'http://feeds.skynews.com/feeds/rss/home.xml',
                # 'cnn': 'http://rss.cnn.com/rss/edition.rss'
            }

@app.route('/browse-headlines', methods=['GET'])
def browse():
    current_user = User.query.filter_by(username=session['username']).first()
    meta = None
    article_pool = None

    for key in RSS_FEEDS:
        feed = feedparser.parse(RSS_FEEDS[key])
        for entry in feed['entries']:
            url_to_scrape = entry.link
            entry_title = entry.title
            entry_summary = entry.summary
            article_exists = ArticlePool.query.filter_by(url=url_to_scrape).first()
            # if entries are not already in ArticlePool, add them
            if not article_exists or article_exists.url != url_to_scrape:
                # add new
                meta = article_meta_scrape(current_user, url_to_scrape)

                title = meta['title']
                description = meta['description']
                url = meta['url']
                image = meta['image']
                source = meta['source']
                slug = slugify(title)
                published_on = entry.published

                article_pool = ArticlePool(
                    url,
                    title,
                    description,
                    None,
                    image,
                    None,
                    published_on,
                    0,
                    0,
                    source,
                    slug
                )

                db.session.add(article_pool)
                db.session.commit()

    articles = ArticlePool.query.order_by('published_on desc')

    return render_template('articlepool/browse.html', articles=articles, current_user=current_user, Bookmark=Bookmark)

@app.route('/browse-headlines/<articleId>', methods=['GET'])
def view_browse_article(articleId):
    # TODO: fix 'post' in view.html
    article_pool = ArticlePool.query.filter_by(id=articleId).first()
    current_user = User.query.filter_by(username=session['username']).first()
    live_comment_form = LiveCommentForm()

    # determine which scraping tools to use
    if article_pool.source == 'BBC News':
        article = bbc_article_content_scrape(article_pool.url)
    elif article_pool.source == 'Sky News':
        article = '<h1>NOpe</h1>'
    else:
        article = '<h1>NOpe</h1>'

    live_comments = LiveComment.query.filter_by(article_pool_id=articleId)

    return render_template('articlepool/view.html', live_comment_form=live_comment_form, article_pool=article_pool, article=article, live_comments=live_comments, current_user=current_user, User=User)


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


@app.route('/browse-headlines/<articleId>/like', methods=['POST'])
def increment_browse_like(articleId):
    """ Social-Feed Post method to increment number of likes """
    article_pool = ArticlePool.query.filter_by(id=articleId).first()
    article_pool.likes += 1
    db.session.commit()
    return redirect(url_for('view_browse_article', articleId=articleId))


@app.route('/browse-headlines/<articleId>/dislike', methods=['POST'])
def increment_browse_dislike(articleId):
    """ Social-Feed Post method to increment number of dislikes """
    article_pool = ArticlePool.query.filter_by(id=articleId).first()
    article_pool.dislikes += 1
    db.session.commit()
    return redirect(url_for('view_browse_article', articleId=articleId))


@app.route('/browse-headlines/<articleId>/comment', methods=['POST'])
def browse_comment(articleId):
    current_user = User.query.filter_by(username=session['username']).first()
    live_comment_form = LiveCommentForm()

    if live_comment_form.validate_on_submit():
        form_comment = live_comment_form.comment.data

        live_comment = LiveComment(
            articleId,
            current_user.id,
            datetime.utcnow(),
            form_comment
        )

        db.session.add(live_comment)
        db.session.flush()

        # TODO: increment num_comments

        db.session.commit()

    return redirect(url_for('view_browse_article', articleId=articleId))
