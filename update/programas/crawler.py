import requests
from bs4 import BeautifulSoup

url = "https://www.reuters.com/markets/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")
