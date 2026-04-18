from scrapers.base_scraper import BaseScraper

class GenericScraper(BaseScraper):
    def fetch(self, url):
        return super().fetch(url)
