import xmltodict
from typing import List
from src.core.serializer import Serializer
from src.core.client import HTTPClient
from src.models.source import Source


class Scraper:

    def scrape(self, url: str, force_thumbnails=False) -> List[dict]:
        print(f'Fetching news from : {url}', end='')
        articles = self._fetch_articles(url, force_thumbnails)
        if articles:
            print(f' -> Success ✅ ')
        else:
            print(f' -> Failed ❌ ')
        return articles

    def scrape_all(self, url_list: List[str], force_thumbnails=False) -> List[List[dict]]:
        all_articles = list()
        for url in url_list:
            articles = self.scrape(url, force_thumbnails)
            if articles:
                all_articles.append(articles)
        return all_articles

    def _fetch_articles(self, url: str, force_thumbnails=False):
        rss_data = self._fetch_rss_data(url)
        if not rss_data:
            return []

        # Setup General Info and the serializer
        name = rss_data['title']
        home_url = rss_data['link']
        # Source
        source = Source(name=name,
                        link=home_url).to_dict()
        # Serializer
        serializer = Serializer(name=name,
                                source=source,
                                force_thumbnails=force_thumbnails)
        # Raw articles
        raw_articles = rss_data['item']
        if not raw_articles:
            return []
        # Serialize the articles
        try:
            articles = serializer.serialize_articles(raw_articles)
            return articles
        except Exception as e:
            print(f"Failed to serialize {name} articles, {e}")
            return []

    @staticmethod
    def _fetch_rss_data(url: str) -> dict | None:
        response = HTTPClient.request(url)
        if not response:
            return None
        # Base rss  data
        try:
            data = xmltodict.parse(response.text)['rss']['channel']
            return data
        except Exception as e:
            print(f'Failed to parse XML to Dict for {url}, {e}')
            return None
