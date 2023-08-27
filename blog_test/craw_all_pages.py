import url_manager
import requests
from bs4 import BeautifulSoup
#sys.path.append("/home/ori/spider/")
import re

root_url = "http://www.crazyant.net"

urls = url_manager.UrlManager()
urls.add_new_url(root_url)

#对当前URL进行操作：写入txt文件，打印输出内容
fout = open("craw_all_pages.txt","w")
#整个while为一个大循环，实现了从拿取新的URL，到新增URL的循环，直到URL池为空
while urls.has_new_url():
    curr_url = urls.get_url()
    r = requests.get(curr_url, timeout = 3)
    if r.status_code != 200:
        print("error, return status_code is not 200", curr_url)
        continue
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string

    fout.write("%s\t%s\n"%(curr_url, title))
    fout.flush()
    print("sucess: %s, %s,%d"%(curr_url, title, len(urls.new_urls)))

#URL管理器：发现新的URL并匹配RE，匹配成功则加入URL池
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href is None:
            continue

        pattern = r'^http://www.crazyant.net/\d+.html$'
        if re.match(pattern,href):
            urls.add_new_url(href)


fout.close()





