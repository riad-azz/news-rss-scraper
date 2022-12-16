from src.core.scraper import Scraper

if __name__ == '__main__':
    scraper = Scraper()
    articles = scraper.scrape('https://www.michaelwest.com.au/feed/')
