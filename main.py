import argparse
from scrapers.generic_scraper import GenericScraper
from parsers.generic_parser import parse_page
from pipelines.cleaner import clean_data
from storage.save_json import save_json
from storage.save_csv import save_csv
from storage.save_excel import save_excel
from storage.save_txt import save_txt
from storage.save_pdf import save_pdf

FORMATS = {
    "json":  (save_json,  "json"),
    "csv":   (save_csv,   "csv"),
    "excel": (save_excel, "xlsx"),
    "xlsx":  (save_excel, "xlsx"),
    "txt":   (save_txt,   "txt"),
    "text":  (save_txt,   "txt"),
    "pdf":   (save_pdf,   "pdf"),
}


def _pick_format():
    choices = "/".join(FORMATS.keys())
    while True:
        fmt = input(f"Output format ({choices}): ").strip().lower()
        if fmt in FORMATS:
            return fmt
        print(f"  Please choose one of: {choices}")


def _run_url_mode(url, fmt, selector, output):
    save_fn, ext = FORMATS[fmt]
    path = output or f"data/processed/output.{ext}"

    print(f"Scraping  : {url}")
    html = GenericScraper().fetch(url)
    if not html:
        print("Failed to fetch the page.")
        return

    print("Parsing   : extracting content...")
    data = parse_page(html, selector=selector)
    if not data:
        print("No data extracted. Try --selector to target specific elements.")
        return

    cleaned = clean_data(data)
    print(f"Records   : {len(cleaned)} extracted")
    save_fn(cleaned, path)


def _run_query_mode(query, fmt, output):
    from intelligence.orchestrator import run_query
    from intelligence.query_parser import parse_query

    save_fn, ext = FORMATS[fmt]
    path = output or f"data/processed/output.{ext}"

    parsed = parse_query(query)
    data = run_query(query, target_count=parsed["count"])
    if not data:
        print("No data could be collected.")
        return

    save_fn(data, path)


def _interactive_mode():
    print("\n=== Web Scraper ===")
    print("1. Scrape a specific URL")
    print("2. Describe what dataset you need (auto-search)")
    choice = input("\nChoose (1 or 2): ").strip()

    fmt = _pick_format()
    output = input("Output file path (leave blank for default): ").strip() or None

    if choice == "1":
        url = input("Enter URL: ").strip()
        selector = input("CSS selector (leave blank to auto-detect): ").strip() or None
        _run_url_mode(url, fmt, selector, output)
    else:
        query = input('\nDescribe the dataset (e.g. "50 Python interview questions"): ').strip()
        _run_query_mode(query, fmt, output)


def main():
    parser = argparse.ArgumentParser(
        description="Web Scraper — provide a URL or just describe what you need.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--url",      help="Specific URL to scrape")
    parser.add_argument("--query",    help='Natural language request e.g. "50 Python interview questions"')
    parser.add_argument("--format",   choices=FORMATS.keys(),
                        help="Output format: json | csv | excel | txt | pdf")
    parser.add_argument("--selector", help="CSS selector to target elements (optional, used with --url)")
    parser.add_argument("--output",   help="Output file path (default: data/processed/output.<ext>)")
    args = parser.parse_args()

    # No args → interactive mode
    if not args.url and not args.query:
        _interactive_mode()
        return

    fmt = args.format or _pick_format()

    if args.query:
        _run_query_mode(args.query, fmt, args.output)
    else:
        _run_url_mode(args.url, fmt, args.selector, args.output)


if __name__ == "__main__":
    main()
