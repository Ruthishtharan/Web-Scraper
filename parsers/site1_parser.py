from bs4 import BeautifulSoup

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []

    for quote in soup.select(".quote"):
        text = quote.select_one(".text").get_text()
        author = quote.select_one(".author").get_text()

        data.append({
            "type": "quote",
            "text": text,
            "author": author
        })

    return data