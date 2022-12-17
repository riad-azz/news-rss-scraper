import json
from typing import List

from src.core.scraper import Scraper

SOURCES = [
    "https://www.dailytelegraph.com.au/news/breaking-news/rss",
    "https://www.smh.com.au/rss/feed.xml",
    "https://www.heraldsun.com.au/news/breaking-news/rss",
    "https://www.abc.net.au/news/feed/1948/rss.xml",
    "https://www.theage.com.au/rss/feed.xml",
    "https://www.couriermail.com.au/rss",
    "https://www.perthnow.com.au/news/feed",
    "https://www.canberratimes.com.au/rss.xml",
    "https://www.brisbanetimes.com.au/rss/feed.xml",
    "http://feeds.feedburner.com/IndependentAustralia",
    "https://www.businessnews.com.au/rssfeed/latest.rss",
    "https://indaily.com.au/feed/",
    "https://www.themercury.com.au/rss",
    "https://feeds.feedburner.com/com/rCTl",
    "http://rssfeeds.9news.com/kusa/home&x=1",
    "https://www.michaelwest.com.au/feed/"
]


def test_scrape_all(sources: List[str], force_thumbnails=False) -> None:
    scraper = Scraper()
    all_articles = scraper.scrape_all(url_list=sources,
                                      force_thumbnails=force_thumbnails)
    assert len(all_articles) > 0, 'The scraper did not fetch any articles'
    for i, articles in enumerate(all_articles):
        with open(f'source_{i}' + '.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2)


def test_scrape(url: str, force_thumbnails=False, filename='test.json'):
    scraper = Scraper()
    articles = scraper.scrape(url=url,
                              force_thumbnails=force_thumbnails)
    assert len(articles) > 0, 'The scraper did not fetch articles'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)
    [print(x) for x in articles]


def test_force_thumbnail(url: str, force_thumbnails=True):
    """
    The RSS feed must not contain any media for this test to be reliable
    since the serializer always tries to fetch the thumbnail from the XML
    before it tries to force fetch from the article page
    """
    scraper = Scraper()
    articles = scraper.scrape(url=url,
                              force_thumbnails=force_thumbnails)
    [print(x['thumbnail']) for x in articles]
    assert all(x['thumbnail'] for x in articles), 'Failed to fetch thumbnails'


if __name__ == '__main__':
    test_scrape('https://www.dailytelegraph.com.au/news/breaking-news/rss', True)
