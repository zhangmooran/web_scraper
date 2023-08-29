import requests
from bs4 import BeautifulSoup
import pprint
import json
import pandas as pd

#构造分页数字列表
page_indexs = range(0, 250, 25)
list(page_indexs)

def download_all_htmls():
    """
    下载所有列表页面的HTML，用于后续分析
    """
    #user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62
    #将user-agent添加到HTTP请求头中
    
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    htmls = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
          'cookie':'bid=_zhfF-ZbaBo; _gid=GA1.2.1119014521.1693273295; ll="108288"; _ga_Y4GN1R87RG=GS1.1.1693273294.1.1.1693273343.0.0.0; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1693273344; Hm_lpvt_19fc7b106453f97b6a84d64302f21a04=1693273344; _ga=GA1.2.618442902.1693273294; _ga_PRH9EWN86K=GS1.2.1693273346.1.0.1693273346.0.0.0; _pk_id.100001.4cf6=f7764ed1b187faa5.1693273366.; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; __yadk_uid=yJHosNbGXoyAIzzidv0xmF3nCvUSTGBx; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1693277239%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DxVyHf7QVWrDzwzEOtf2E5Rw5pNkDBwoJYapsobZd8Yk8vPxuSUan-PP-s6t9JXTE%26wd%3D%26eqid%3D8724702400076e420000000364ed4d11%22%5D; _pk_ses.100001.4cf6=1; dbcl2="155720260:BSgj1oGmpnk"; ck=OimW; __utma=30149280.618442902.1693273294.1693273366.1693277276.2; __utmb=30149280.0.10.1693277276; __utmz=30149280.1693277276.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.618442902.1693273294.1693273366.1693277276.2; __utmb=223695111.0.10.1693277276; __utmz=223695111.1693277276.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'}
    for idx in page_indexs:
        url = f"https://movie.douban.com/top250?start={idx}&filter="
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
          'cookie':'bid=_zhfF-ZbaBo; _gid=GA1.2.1119014521.1693273295; ll="108288"; _ga_Y4GN1R87RG=GS1.1.1693273294.1.1.1693273343.0.0.0; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1693273344; Hm_lpvt_19fc7b106453f97b6a84d64302f21a04=1693273344; _ga=GA1.2.618442902.1693273294; _ga_PRH9EWN86K=GS1.2.1693273346.1.0.1693273346.0.0.0; _pk_id.100001.4cf6=f7764ed1b187faa5.1693273366.; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; __yadk_uid=yJHosNbGXoyAIzzidv0xmF3nCvUSTGBx; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1693277239%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DxVyHf7QVWrDzwzEOtf2E5Rw5pNkDBwoJYapsobZd8Yk8vPxuSUan-PP-s6t9JXTE%26wd%3D%26eqid%3D8724702400076e420000000364ed4d11%22%5D; _pk_ses.100001.4cf6=1; dbcl2="155720260:BSgj1oGmpnk"; ck=OimW; __utma=30149280.618442902.1693273294.1693273366.1693277276.2; __utmb=30149280.0.10.1693277276; __utmz=30149280.1693277276.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.618442902.1693273294.1693273366.1693277276.2; __utmb=223695111.0.10.1693277276; __utmz=223695111.1693277276.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'}
        print("craw html:", url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    return htmls

#执行爬取
htmls = download_all_htmls()
# print(htmls[1])

# 解析HTML得到数据

def parse_single_html(html):
    """
    解析单个HTML，得到数据
    @return list({"link", "title", [lable]})
    """
    soup = BeautifulSoup(html, 'html.parser')
    article_items = (soup.find("div", class_="article")
                         .find("ol", class_="grid_view")
                         .find_all("div", class_="item")
    )
    datas = []
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        info = article_item.find("div", class_="info")
        title = info.find("div", class_="hd").find("span", class_="title").get_text()
        stars = (
            info.find("div", class_="bd")
                .find("div", class_="star")
                .find_all("span")
        )
        rating_star = stars[0]["class"][0]
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()
        
        datas.append({
            "rank":rank,
            "title":title,
            "rating_star":rating_star.replace("rating","").replace("-t",""),
            "rating_num":rating_num,
            "comments":comments.replace("人评价","")
        })
    return datas

# pprint.pprint(parse_single_html(htmls[0]))

# 执行所有HTML页面的解析

all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))

# all_datas
# len(all_datas)

# 将结果存入EXCEL
df = pd.DataFrame(all_datas)
# df
df.to_excel("豆瓣电影TOP250.xlsx")