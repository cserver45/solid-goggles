""" solid-googles: A web scraping script to noify you of new linux releases via RSS.

"""
import bs4
import requests

# for now, this will just get new manjaro versions
# later it will be however many sites I can do
url = "https://manjaro.org/download/"
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, "html.parser")
# for now, this only gets plasma edition and not any of the others
link = soup.find(id="of-full-plasma").find_all("a")[1]
print(link['href'])
