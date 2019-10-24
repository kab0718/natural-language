import application.morpheme_common
import re
import codecs
import pandas as pd
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup
import requests

def file_open(file_name):
    test_data = open(file_name, encoding="utf_8_sig")

    contents = test_data.readlines()
    test_data.close()

    return contents

def create_novel(lines):
    corps = []
    for line in lines:
        text = line
        text = re.sub(r'《.+?》', '', text)  # ルビ削除
        text = re.sub(r'［＃.+?］', '', text)  # 入力者注削除
        corps.append(application.morpheme_common.sharing_text_noun(text))
    # corpsのそれぞれの要素の末尾に改行文字追加
    with codecs.open("input_data.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

def collection_talk_million():
    corps = []
    link = "https://millionlive.info/?北沢志保"
    r = requests.get(link)

    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')

        data = [[[td.get_text(strip=True) for td in trs.select('th, td')]
                 for trs in tables.select('tr')]
                for tables in soup.select('table')]

        print(len(data))
        print(len(data[15]))
        i=2
        pattern = r"「.*」"
        while i < 95:
            text = re.findall(pattern, data[15][i][0])
            if not text:
                pass
            else:
                corps.append(text[0])
            i += 1

    with codecs.open("kitazawa_data2.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

def collection_talk_theater():
    corps = []
    link = "https://imasml-theater-wiki.gamerch.com/北沢志保"
    r = requests.get(link)

    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')

        data = [[[td.get_text(strip=True) for td in trs.select('th, td')]
                for trs in tables.select('tr')]
                for tables in soup.select('table')]

        i=4
        while i < 43:
            j = 1
            while j <= len(data[i])-1:
                text = data[i][j][0]
                text = text.replace('〇〇', '').replace('○○', '')
                text = text.replace('……', '...')
                corps.append(text)
                j += 1
            i += 1

    with codecs.open("kitazawa_data.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

def create_talk(lines):
    corps = []
    for line in lines:
        corps.append(application.morpheme_common.sharing_text_noun(line))

    with codecs.open("kitazawa_input_data2.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

#create_novel(file_open("ningen_shikkaku_syuki2.txt"))
#create_tweet(file_open("tweet.txt"))

collection_talk_million()
create_talk(file_open("kitazawa_data2.txt"))