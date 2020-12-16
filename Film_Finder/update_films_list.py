"""For updating list of films on doramalive.ru"""
from bs4 import BeautifulSoup
import requests
import json
import time

def create_database():
    """Make a dictionary: 'name': 'link' """
    database = {}
    for i in range(1, 122):
        url = f"https://doramalive.ru/dorama/?mode=all&PAGEN_1={i}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        mydivs = soup.find_all("div", class_="media-body")
        for div in mydivs:
            name = div.find("div", class_="media-heading").string
            link = div.find("div", class_="media-heading").find("a").get("href")
            database[name.lower()] = link
        print(f"Страница № {i}")
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    create_database()
    print("Список дорам обновлён!")
    time.sleep(5)
