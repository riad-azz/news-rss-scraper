import json
import argparse
import os.path
from typing import List
from src import Scraper


def save_articles(articles: List[dict], filename: str):
    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)
    path = os.path.abspath(f'./{filename}')
    print(f'{len(articles)} Articles were saved to : {path}')


# --- Arguments Parser ---
parser = argparse.ArgumentParser()
parser.add_argument('--url', help='the rss feed url', required=True, type=str)
parser.add_argument('--force-thumbnails', help='If you would like to try and force fetch thumbnails set this to True',
                    default=False, type=bool)
parser.add_argument('--filename', help='The name of the articles json file', type=str, default='articles')
args = parser.parse_args()
# --- Application Vars ---
feed_url = args.url
force_thumbnails = args.force_thumbnails
filename = args.filename

if __name__ == '__main__':
    scraper = Scraper()
    articles = scraper.scrape(feed_url, force_thumbnails)
    save_articles(articles, filename)
