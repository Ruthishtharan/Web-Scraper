import requests
import time
from config import HEADERS

def get_request(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Retry {attempt+1}: {e}")
            time.sleep(2)
    return None