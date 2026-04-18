import re

NUMBER_WORDS = {
    "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "hundred": 100, "one hundred": 100, "two hundred": 200,
}

STOP_PHRASES = [
    "give me", "i need", "i want", "get me", "fetch", "scrape",
    "find me", "generate", "create", "make", "build", "a dataset of",
    "dataset of", "a set of", "a list of", "list of", "some", "about",
    "questions about", "data about", "info about", "information about",
]


def parse_query(text):
    count = _extract_count(text)
    topic = _extract_topic(text)
    return {"count": count, "topic": topic}


def _extract_count(text):
    match = re.search(r"\b(\d+)\b", text)
    if match:
        return int(match.group(1))
    lower = text.lower()
    for word, val in sorted(NUMBER_WORDS.items(), key=lambda x: -len(x[0])):
        if word in lower:
            return val
    return 50


def _extract_topic(text):
    cleaned = text
    cleaned = re.sub(r"\b\d+\b", "", cleaned)
    for phrase in sorted(STOP_PHRASES, key=len, reverse=True):
        cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip(" .,?!")
