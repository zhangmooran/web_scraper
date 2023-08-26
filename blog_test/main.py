import requests
from bs4 import BeautifulSoup

url = "http://www.crazyant.net"

r = requests.get(url)
if r.status_code != 200:
    raise Exception()

html_doc = r.text

soup = BeautifulSoup(html_doc, "html.parser")
h2_nodes = soup.find_all("h2",class_="entry-title")

for h2_node in h2_nodes:
    link = h2_node.find("a")
    print(link["href"], link.get_text())



