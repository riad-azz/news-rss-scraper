from typing import List
from bs4 import BeautifulSoup
from src.core.client import HTTPClient
from src.models.article import Article
from datetime import datetime


class Serializer:
    def __init__(self, name: str, source: dict, force_thumbnails: bool):
        self.name = name
        self.source = source
        self.force_thumbnails = force_thumbnails

    def serialize_articles(self, articles_list: List[dict]) -> List[dict]:
        articles = [x for x in self._serialize_articles(articles_list)]
        return articles

    def _serialize_articles(self, articles_list: List[dict]) -> List[dict]:
        for item in articles_list:
            # Title
            try:
                title = self.html_to_string(item['title'])
            except Exception as e:
                print(f"Problem extracting title from {self.name}, {e}")
                continue
            # Link
            try:
                link = self._get_link(item)
            except Exception as e:
                print(f"Problem extracting link from {self.name}, {e}")
                continue
            # Description
            try:
                description = self.html_to_string(item.get('description', ''))
            except Exception as e:
                print(f"Problem extracting description from {self.name}, {e}")
                continue
            # Thumbnail
            try:
                thumbnail = self._get_thumbnail(item)
            except Exception as e:
                print(f"Problem extracting thumbnail from {self.name}, {e}")
                continue
            # Publish date
            try:
                published = item.get('pubDate', '')
            except Exception as e:
                print(f"Problem extracting publish date from {self.name}, {e}")
                continue

            # Some articles might not have a publishing date, so I included the fetching date
            date_format = "%a, %d %b %Y %H:%M:%S %z"
            fetched_date = datetime.now().strftime(date_format)
            article = Article(
                title=title,
                link=link,
                description=description,
                thumbnail=thumbnail,
                source=self.source,
                publish_date=published,
                fetched_date=fetched_date)

            yield article.to_dict()

    @staticmethod
    def _get_link(item) -> str:
        link = item.get('link', None)
        if link:
            return link
        guid_link = item['guid']['#text']
        return guid_link

    def _get_thumbnail(self, item) -> str:
        # -- Try to get thumbnail from the XML --
        image_url = ''
        # From media
        media = item.get('media:content', None)
        if media:
            image_url = self.image_from_xml(media)
        # From enclosure
        enclosure = item.get('enclosure', None)
        if enclosure:
            image_url = self.image_from_xml(enclosure)
        # -- Try to get the thumbnail from the article page --
        # works only if forced thumbnail is set to True
        if self.force_thumbnails and not image_url:
            html_page = HTTPClient.fetch_html_page(item['link'])
            if html_page:
                image_url = self._fetch_thumbnail(html_page)

        return image_url

    @staticmethod
    def image_from_xml(media) -> str:
        image_url = ''
        if type(media) is list:
            for content in media:
                if 'image' in content.get('@type', ''):
                    image_url = content.get('@url', '')
                    break
        else:
            if 'image' in media.get('@type', ''):
                image_url = media.get('@url', '')
        return image_url

    @staticmethod
    def _fetch_thumbnail(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('meta', {'property': 'og:image'})
        try:
            return image.get('content')
        except:
            return ''

    @staticmethod
    def html_to_string(html: str) -> str:
        """
        Decode all html encodings and remove html elements
        :param html: html code as str
        :return: str without html encoding
        """
        html_obj = BeautifulSoup(html, 'html.parser')
        text = html_obj.text.encode("ascii", "ignore").decode()
        if text:
            text = text.replace('[]', '')
        return text
