from utils.request_handler import get_request

class BaseScraper:
    def fetch(self, url):
        return get_request(url)