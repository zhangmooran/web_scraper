url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
    "User-Agent" : """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"""
}


import requests
import pandas as pd

def craw_table(year, month):
    """
    提供年份和月份爬取对应的表格数据
    """
    params = {
    "areaInfo[areaId]": 54511,
    "areaInfo[areaType]": 2,
    "date[year]": year,
    "date[month]": month
}

    resp = requests.get(url, headers=headers, params=params)
    # print(resp.status_code)
    data = resp.json()["data"]
    # print(data)
    df = pd.read_html(data)[0]
    # html中有table标签，故需要lxml库解析表格
    return df

df_list = []
for year in range(2011, 2022):
    for month in range(1, 13):
        print("爬取：", year, month)
        df = craw_table(year, month)
        df_list.append(df)

pd.concat(df_list).to_excel("WeathersInBeijingForTenYears.xlsx", index=False)