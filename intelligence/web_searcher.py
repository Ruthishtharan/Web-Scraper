from ddgs import DDGS

TRUSTED_SITES = [
    "geeksforgeeks.org",
    "interviewbit.com",
    "javatpoint.com",
    "tutorialspoint.com",
    "guru99.com",
    "simplilearn.com",
    "edureka.co",
    "intellipaat.com",
    "hackerrank.com",
    "indeed.com",
]


def search_urls(topic, max_urls=8):
    queries = [
        f"{topic} interview questions and answers",
        f"top {topic} interview questions",
        f"{topic} questions answers site:geeksforgeeks.org OR site:interviewbit.com OR site:javatpoint.com",
    ]

    urls = []
    seen = set()

    with DDGS() as ddgs:
        for query in queries:
            try:
                results = ddgs.text(query, max_results=6)
                for r in results:
                    url = r.get("href", "")
                    if not url or url in seen:
                        continue
                    seen.add(url)
                    if any(site in url for site in TRUSTED_SITES):
                        urls.insert(0, url)
                    else:
                        urls.append(url)
                    if len(urls) >= max_urls:
                        return urls
            except Exception:
                continue

    return urls[:max_urls]
