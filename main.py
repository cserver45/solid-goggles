""" solid-googles: A web scraping script to noify you of new linux releases via RSS.

"""
import os
from datetime import datetime, timezone
import shutil
import json
import bs4
import requests
import xmltodict


def send_rss(latest: dict, old: dict):
    """Add the entry to the rss file."""

    if os.path.isfile('feed.rss') is False:
        shutil.copy("template.rss", "feed.rss")

    with open("feed.rss", "r") as f:
        rss_feed = xmltodict.parse(f.read())

    for key, value in latest.items():
        # turn this to != after testing done
        if value == old[key]:
            # later ill do some kind of matching so the name looks right
            item = {
                "title": f"New ISO Release: {key}",
                "description": {
                    "p": {
                        "a": {
                            "@href": value,
                            "#text": "ISO Link"
                        },
                        "p": {
                            "#text": f"New Release of {key}!"
                        }
                    }
                },
                "link": value,
                "author": "no-reply@localhost",
                "pubDate": datetime.now(tz=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z"),
                "guid": value
            }
            try:
                rss_feed['rss']['channel']['item'].append(item)
            except KeyError:
                rss_feed['rss']['channel']['item'] = [item]

    rss_str = xmltodict.unparse(rss_feed, pretty=True)
    with open("feed.rss", "w") as f:
        f.write(rss_str.replace('<?xml version="1.0" encoding="utf-8"?>\n', ''))

# for now, this will just get new manjaro versions
# later it will be however many sites I can do
url = "https://manjaro.org/download/"
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, "html.parser")
# for now, this only gets plasma edition and not any of the others
manjaro_offical_isos = ['of-full-plasma', 'of-full-xfce', 'of-full-gnome']
manjaro_json = {}
for rel in manjaro_offical_isos:
    link = soup.find(id=rel).find_all("a")[1]['href']
    manjaro_json[rel] = link

# we wil write the previous value to the file if the file doesn't exist
# that indicates the script has not run once yet
# and yes, json files are not the best, but I don't feel like setting up a proper db
if os.path.isfile('manjaro.json') is False:
    with open('manjaro.json', 'w') as f:
        json.dump(manjaro_json, f)
    manjaro_entries = manjaro_json
else:
    with open('manjaro.json', 'r') as f:
        manjaro_entries = json.load(f)

if manjaro_json != manjaro_entries:
    print('update found')
    # update the file for the next run
    with open('manjaro.json', 'w') as f:
        json.dump(manjaro_json, f)
    # send a message via rss
# indent below after testing is done
send_rss(manjaro_json, manjaro_entries)

