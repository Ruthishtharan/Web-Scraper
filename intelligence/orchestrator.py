from intelligence.query_parser import parse_query
from intelligence.web_searcher import search_urls
from scrapers.generic_scraper import GenericScraper
from parsers.generic_parser import parse_page
from pipelines.cleaner import clean_data


def run_query(query_text, target_count=None):
    parsed = parse_query(query_text)
    topic = parsed["topic"]
    count = target_count or parsed["count"]

    print(f"Topic     : {topic}")
    print(f"Target    : {count} records")
    print("Searching : finding relevant websites...")

    urls = search_urls(topic)
    if not urls:
        print("No relevant websites found.")
        return []

    print(f"Found     : {len(urls)} websites to try\n")

    scraper = GenericScraper()
    all_data = []
    seen_keys = set()

    for i, url in enumerate(urls, 1):
        if len(all_data) >= count:
            break

        print(f"[{i}/{len(urls)}] Scraping: {url}")
        html = scraper.fetch(url)
        if not html:
            print("       -> Failed to fetch, skipping")
            continue

        records = parse_page(html)
        cleaned = clean_data(records)

        added = 0
        for record in cleaned:
            if len(all_data) >= count:
                break
            key = (record.get("question") or record.get("text") or "")[:60].lower().strip()
            if key and key not in seen_keys:
                seen_keys.add(key)
                all_data.append(record)
                added += 1

        print(f"       -> Got {added} new records (total: {len(all_data)}/{count})")

    print(f"\nDone. Collected {len(all_data)} records.")
    return all_data
