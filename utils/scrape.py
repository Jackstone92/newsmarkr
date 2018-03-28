# import modules for scraping
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def article_meta_scrape(current_user, url):
    # web scrape
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    title = soup.find('meta', property='og:title')
    description = soup.find('meta', property='og:description')
    url = soup.find('meta', property='og:url')
    image = soup.find('meta', property='og:image')
    src = soup.find('meta', property='og:site_name')

    # meta dictionary to hold scraped data
    meta = {}
    meta['title'] = title['content'] if title else 'err'
    meta['description'] = description['content'] if description else 'err'
    meta['url'] = url['content'] if url else 'err'
    meta['image'] = image['content'] if image else 'err'
    meta['source'] = src['content'] if source else 'err'

    return meta

def article_content_scrape(url):
    # web scrape
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml').prettify()

    return soup


def bbc_article_content_scrape(url):
    # web scrape
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    article = soup.find(class_='story-body__inner')

    if article:
        return soup.prettify()

    return soup.get_text()
    # TODO:
    # get images and format
    # get header tags and format
    # get content and format
