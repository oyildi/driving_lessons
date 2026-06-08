import os
import requests
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

username = "NeedhamDriving"

user_id = 426716224

STATE_FILE = "last_seen.txt"

# url = f"https://api.x.com/2/users/by/username/{username}"

# r = requests.get(url, headers=headers)

# print(r.json())


def get_latest_tweet():
    url = f"https://api.x.com/2/users/{user_id}/tweets?max_results=5"
    r = requests.get(url, headers=headers)
    return r.json()["data"][0]


def load_last_seen():
    if not os.path.exists(STATE_FILE):
        return None
    return open(STATE_FILE).read().strip()


def save_last_seen(tweet_id):
    with open(STATE_FILE, "w") as f:
        f.write(tweet_id)

