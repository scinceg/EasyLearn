# This is the way
# Author: pythontoday
# YouTube: https://www.youtube.com/c/PythonToday/videos

import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
from data_base import sqlite_db

# url = "https://ria.ru/keyword_anglijjskijj_jazyk/"
# #
# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
# }
# #
# req = requests.get(url, headers=headers)
# src = req.text
# print(src)

# with open("Projects\Python\Bots\EasyLearn\parsing\index.html", "w", encoding="utf-8") as file:
#     file.write(src)

# сохранить линкс в бд
# 
def parst_start():
    with open("Projects\Python\Bots\EasyLearn\parsing\index.html", encoding="utf-8") as file:
        src = file.read()

    print('Parsing is working too')
    global titles, links
    titles = []
    links = []

    soup = BeautifulSoup(src, "lxml")
    all_news_div = soup.find_all(class_="list-item")
    i = 1
    for item in all_news_div[:5]:
        item_text = item.text
        titles.append(item_text)
        lnk = item.source.get('srcset')
        with open("Projects\Python\Bots\EasyLearn\parsing\images\image{0}.png".format(i),"wb") as f:
            f.write(requests.get(lnk).content)
        i+=1
        href = item.a.get('href')
        links.append(href)
    return links, titles
    # sqlite_db.sql_add_pars_data(titles, links)