import requests
from bs4 import BeautifulSoup

url = "https://bongda24h.vn/vck-world-cup/ket-qua-41.html"
domain = 'https://bongda24h.vn'

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
items = soup.find_all("div", class_="item-other4")

link_matchs = []
for item in items:
    url = item.find("a")["href"]
    link_matchs.append(domain + url)
# remove duplicate matches
link_matchs = link_matchs[4:]
with open("data/links.txt", "w") as f:
    for link in link_matchs:
        f.write(link + "\n")