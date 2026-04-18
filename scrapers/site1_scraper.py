from scrapers.base_scraper import BaseScraper
from parsers.site1_parser import parse_quotes
from config import SITE1_URL

class Site1Scraper(BaseScraper):
    def run(self):
        html = self.fetch(SITE1_URL)
        return parse_quotes(html)