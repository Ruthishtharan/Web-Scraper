import re
from bs4 import BeautifulSoup

QUESTION_HEADING_TAGS = ["h2", "h3", "h4", "h5"]
ANSWER_TAGS = {"p", "ul", "ol", "pre", "code", "blockquote", "div", "table"}


def parse_page(html, selector=None):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    if selector:
        return _parse_by_selector(soup, selector)

    # Try interview Q&A detection first
    qa = _parse_interview_questions(soup)
    if qa:
        return qa

    # Fall back to tables
    tables = soup.find_all("table")
    if tables:
        data = _parse_tables(tables)
        if data:
            return data

    # Then lists
    lists = [l for l in soup.find_all(["ul", "ol"]) if len(l.find_all("li")) > 3]
    if lists:
        data = _parse_lists(lists)
        if data:
            return data

    return _parse_text_blocks(soup)


# ── Interview Q&A ──────────────────────────────────────────────────────────────

def _is_question(text):
    text = text.strip()
    if len(text) < 8 or len(text) > 300:
        return False
    patterns = [
        r'^\d+[\.\)\-]\s',                           # "1. ..." / "1) ..."
        r'^Q\s*\d*[\.\):\s]',                         # "Q1." / "Q:"
        r'\?$',                                        # ends with ?
        r'^(What|How|Why|When|Where|Which|Who|'
        r'Explain|Describe|Define|List|Difference|'
        r'Tell me|Can you|Is |Are |Do |Does )',        # common openers
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def _clean_question(text):
    text = re.sub(r'^\d+[\.\)\-]\s*', '', text.strip())
    text = re.sub(r'^Q\s*\d*[\.\):\s]+', '', text, flags=re.IGNORECASE)
    return text.strip()


def _collect_answer(question_tag, all_question_tags):
    q_set = set(id(t) for t in all_question_tags)
    parts = []
    for sib in question_tag.next_siblings:
        if not hasattr(sib, "name"):
            continue
        if id(sib) in q_set or sib.name in QUESTION_HEADING_TAGS:
            break
        if sib.name in ANSWER_TAGS:
            text = sib.get_text(separator=" ", strip=True)
            if text and len(text) > 3:
                parts.append(text)
    return " ".join(parts)


def _parse_interview_questions(soup):
    candidates = [
        tag for tag in soup.find_all(QUESTION_HEADING_TAGS)
        if _is_question(tag.get_text(strip=True))
    ]
    if len(candidates) < 3:
        return []

    data = []
    for tag in candidates:
        question = _clean_question(tag.get_text(strip=True))
        answer = _collect_answer(tag, candidates)
        if question:
            entry = {"question": question}
            if answer:
                entry["answer"] = answer
            data.append(entry)
    return data


# ── CSS selector ───────────────────────────────────────────────────────────────

def _parse_by_selector(soup, selector):
    elements = soup.select(selector)
    data = []
    for el in elements:
        item = {}
        children = el.find_all(True, recursive=False)
        if children:
            for child in children:
                text = child.get_text(strip=True)
                if not text:
                    continue
                key = (child.get("class") or [child.name])[0]
                base = key
                i = 1
                while key in item:
                    key = f"{base}_{i}"
                    i += 1
                item[key] = text
        if not item:
            text = el.get_text(strip=True)
            if text:
                item = {"text": text}
        if item:
            data.append(item)
    return data


# ── Tables ─────────────────────────────────────────────────────────────────────

def _parse_tables(tables):
    data = []
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if not cells or all(c.name == "th" for c in cells):
                continue
            texts = [c.get_text(strip=True) for c in cells]
            item = dict(zip(headers, texts)) if headers else {f"col_{i}": t for i, t in enumerate(texts)}
            if any(item.values()):
                data.append(item)
    return data


# ── Lists ──────────────────────────────────────────────────────────────────────

def _parse_lists(lists):
    data = []
    for lst in lists:
        for li in lst.find_all("li"):
            text = li.get_text(strip=True)
            if not text:
                continue
            links = [a.get("href", "") for a in li.find_all("a")]
            item = {"text": text}
            if links:
                item["links"] = ", ".join(links)
            data.append(item)
    return data


# ── Text blocks fallback ───────────────────────────────────────────────────────

def _parse_text_blocks(soup):
    data = []
    main = soup.find("main") or soup.find("article") or soup.find("body")
    if not main:
        return data
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "a"]):
        text = el.get_text(strip=True)
        if not text or len(text) < 5:
            continue
        item = {"tag": el.name, "text": text}
        if el.name == "a" and el.get("href"):
            item["href"] = el["href"]
        data.append(item)
    return data
