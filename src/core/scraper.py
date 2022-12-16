import requests
import xmltodict
from typing import List
from src.core.serializer import Serializer
from src.models.source import Source
from src.utils import user_agent


class Scraper:

    def fetch_articles(self, url: str, force_thumbnails=False) -> List[dict]:
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

    def _fetch_rss_data(self, url: str) -> dict | None:
        response = self.request(url)
        if not response:
            return None
        # Base rss  data
        try:
            data = xmltodict.parse(response.text)['rss']['channel']
            return data
        except Exception as e:
            print(f'Failed to parse XML to Dict, {e}')
            return None

    @staticmethod
    def _fetch_html_page(link: str) -> str | None:
        response = Scraper.request(link)
        if not response:
            return None
        return response.text

    @staticmethod
    def request(url: str, timeout: int = 10) -> requests.Response | None:
        try:
            response = requests.get(url=url,
                                    headers={'User-Agent': user_agent()},
                                    timeout=timeout)
        except Exception as e:
            print(f"Couldn't connect to {url}, {e}")
            return None

        if response.status_code != 200:
            print(f'Bad status code : {response.status_code}, {url}')
            return None

        return response
