# News RSS Scraper

Scrape news from any RSS feed with ease

## Description

Very simple and easy to use scraper to get RSS feeds by simply using the XML link.
You can use it to create APIs or personal use to save the news or whatever suits your needs.
It should work with any RSS feed with no problem.

If you face any errors feel free to contact me and let me know.

Don't forget to hit the ⭐, If you like this repo
## Getting Started

### Dependencies

* [Python 3.11.0](https://www.python.org/)
* [Requests library](https://requests.readthedocs.io/en/latest/)
* [Beautiful Soup 4 library](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [XML to dict library](https://pypi.org/project/xmltodict/)

### Installing

* How to download the repository
```
git clone https://github.com/riad-azz/news-rss-scraper.git
```

### Executing program


* To scrape the news all you have to do is call `scrape(url)` and pass the rss feed url.
```python
from src import Scraper

scraper = Scraper()
articles = scraper.scrape(url='https://www.dailytelegraph.com.au/news/breaking-news/rss')
```

* Some rss feeds do not include a thumbnail, BUT! you can use __force_thumbnails__ to try and get the thumbnail from the article page.
 
```python
from src import Scraper

scraper = Scraper()
articles = scraper.scrape(url='https://www.dailytelegraph.com.au/news/breaking-news/rss',
                          force_thumbnails=True)
```
_Note that it will take a bit longer to finish because it makes a get request to every article page in the rss feed_.


* You also have the option to scrape from multiple feeds at the same time, all you need to do is make a list of the feeds you would like to scrape and call `scrape_all(url_list)` passing the list of urls.

```python
from src import Scraper

rss_feeds = [
    "https://www.dailytelegraph.com.au/news/breaking-news/rss",
    "https://www.smh.com.au/rss/feed.xml",
    "https://www.heraldsun.com.au/news/breaking-news/rss",
    "https://www.abc.net.au/news/feed/1948/rss.xml",
    "https://www.theage.com.au/rss/feed.xml",
    "https://www.couriermail.com.au/rss",
    "https://www.perthnow.com.au/news/feed",
]

scraper = Scraper()
rss_articles = scraper.scrape_all(url_list=rss_feeds,
                          force_thumbnails=True)
```
_This will return a List of articles Lists like so `List[List[dict]]`, and as shown in the example above you can use __force_thumbnails__ here too_.

* Last but not least you can use the command prompt which works for one feed at a time only
```
python run.py --url='https://indaily.com.au/feed/' --force-thumbnails=True --filename='articles'
```

* You can find a json example of the articles in "_example.json_", and here is a article object example:
```json
{
    "id": "0",
    "title": "article title",
    "link": "https://article-url-example.com/article_id",
    "thumbnail": "https://article-url-example.com/article_thumbnail.jpg",
    "description": "article description",
    "source": {
      "id": "0",
      "link": "https://article-url-example.com/",
      "name": "source name"
    },
    "publish_date": "Sat, 17 Dec 2022 11:23:11 +0000",
    "fetched_date": "Sat, 17 Dec 2022 02:16:23 "
}
```

## Version History

* 1.0.0
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

The rss feeds used in the tests are from a great repository filled with feeds from different countries:
* [Awesome RSS Feeds](https://github.com/plenaryapp/awesome-rss-feeds) by [ plenaryapp ](https://github.com/plenaryapp)
