""" solid-googles: A web scraping script to noify you of new linux releases via RSS.

"""
import os
import json
import bs4
import requests

# for now, this will just get new manjaro versions
# later it will be however many sites I can do
url = "https://manjaro.org/download/"
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, "html.parser")
# for now, this only gets plasma edition and not any of the others
link = soup.find(id="of-full-plasma").find_all("a")[1]['href']

# later this will add all entries to the file while being run in a for loop
manjaro_json = {'plasma': link}
# we wil write the previous value to the file if the file doesn't exist
# that indicates the script has not run once yet
# and yes, json files are not the best, but I don't feel like setting up a proper db
if os.path.isfile('manjaro.json') is False:
    with open('manjaro.json', 'w', encoding='UTF-8') as f:
        f.write(json.dump(manjaro_json))
    manjaro_entries = manjaro_json
else:
    with open('manjaro.json', 'r') as f:
        manjaro_entries = json.loads(f.read())

