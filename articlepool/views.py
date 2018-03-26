from flask_newsmarkr import app
from flask import render_template, redirect, flash, url_for, session, abort, request

# feedparser for parsing rss feeds
import feedparser

from utils.scrape import article_meta_scrape, article_content_scrape

# dictionary of rss feed urls
RSS_FEEDS = {
                'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'sky_home': 'http://feeds.skynews.com/feeds/rss/home.xml',
                'cnn': 'http://rss.cnn.com/rss/edition.rss'
            }

@app.route('/browse-headlines')
def browse():
    articles = []
    publication = 'bbc'

    for key in RSS_FEEDS:
        feed = feedparser.parse(RSS_FEEDS[key])
        for entry in feed['entries']:
            articles.append(entry)

    return render_template('articlepool/browse.html', articles=articles)
