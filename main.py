import json

import requests
import xmltodict as xd

from src.core.scraper import Scraper

scraper = Scraper()
sources = [
    "https://www.dailytelegraph.com.au/news/breaking-news/rss",
    # "https://www.smh.com.au/rss/feed.xml",
    # "https://www.heraldsun.com.au/news/breaking-news/rss",
    # "https://www.abc.net.au/news/feed/1948/rss.xml",
    # "https://www.theage.com.au/rss/feed.xml",
    # "https://www.couriermail.com.au/rss",
    # "https://www.perthnow.com.au/news/feed",
    # "https://www.canberratimes.com.au/rss.xml",
    # "https://www.brisbanetimes.com.au/rss/feed.xml",
    # "http://feeds.feedburner.com/IndependentAustralia",
    # "https://www.businessnews.com.au/rssfeed/latest.rss",
    # "https://indaily.com.au/feed/",
    # "https://www.themercury.com.au/rss",
    # "https://feeds.feedburner.com/com/rCTl",
    # "http://rssfeeds.9news.com/kusa/home&x=1",
    # "https://www.michaelwest.com.au/feed/"
]

articles = scraper.fetch_articles(sources[0], force_thumbnails=True)

with open('test.json', 'w') as f:
    json.dump(articles, f)
