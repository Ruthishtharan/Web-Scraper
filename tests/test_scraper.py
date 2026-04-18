from scrapers.site1_scraper import Site1Scraper

def test_scraper():
    scraper = Site1Scraper()
    data = scraper.run()

    assert isinstance(data, list)
    assert len(data) > 0