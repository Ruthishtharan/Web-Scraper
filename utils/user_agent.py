import random

USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/120.0",
    "Safari/537.36"
]

def get_user_agent():
    return random.choice(USER_AGENTS)