from scrapers.base_scraper import BaseScraper
from parsers.site2_parser import parse_books
from config import SITE2_URL

class Site2Scraper(BaseScraper):
    def run(self):
        html = self.fetch(SITE2_URL)
        return parse_books(html)