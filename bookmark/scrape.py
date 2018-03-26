# import modules for scraping
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def article_meta_scrape(current_user, url):
    # web scrape
    source = requests.get(url).text
    s = BeautifulSoup(source, 'lxml')
    title = s.find('meta', property='og:title')
    description = s.find('meta', property='og:description')
    url = s.find('meta', property='og:url')
    image = s.find('meta', property='og:image')
    source = s.find('meta', property='og:site_name')

    # meta dictionary to hold scraped data
    meta = {}
    meta['title'] = title['content'] if title else 'err'
    meta['description'] = description['content'] if description else 'err'
    meta['url'] = url['content'] if url else 'err'
    meta['image'] = image['content'] if image else 'err'
    meta['source'] = source['content'] if source else 'err'

    return meta
