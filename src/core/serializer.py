from typing import List
from bs4 import BeautifulSoup
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
                description = self.html_to_string(item['description'])
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
                backup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                published = item.get('pubDate', backup_date)
            except Exception as e:
                print(f"Problem extracting publish date from {self.name}, {e}")
                continue

            article = Article(
                title=title,
                link=link,
                description=description,
                thumbnail=thumbnail,
                source=self.source,
                publish_date=published)

            yield article.to_dict()

    @staticmethod
    def _get_link(item) -> str:
        link = item.get('link', None)
        if link:
            return link
        guid_link = item['guid']['#text']
        return guid_link

    @staticmethod
    def _get_thumbnail(item) -> str:
        #TODO: FINISH THIS RIGHT NOW
        # Return the fetched thumbnail (works only if FORCED_THUMBNAIL is set to true in the Scraper)
        forced_thumbnail = item.get('thumbnail', None)
        if forced_thumbnail:
            return forced_thumbnail

        media = item.get('media:content', None)
        if not media:
            return ''

        if type(media) is list:
            image_url = media[0].get('@url', '')
            return image_url
        else:
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
        text = html_obj.text.encode("ascii", "ignore").decode().replace('[]', '')
        return text
