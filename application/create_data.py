import application.morpheme_common
import re
import codecs
import pandas as pd
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup
import requests
import csv
import glob

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
    link = "https://millionlive.info/?七尾百合子"
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
        while i < 94:
            text = re.findall(pattern, data[15][i][0])
            if not text:
                pass
            else:
                corps.append(text[0])
            i += 1

    with codecs.open("nanao_data2.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

def collection_talk_theater():
    corps = []
    link = "https://imasml-theater-wiki.gamerch.com/七尾百合子"
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

    with codecs.open("nanao_data.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

def create_talk(lines):
    corps = []
    for line in lines:
        corps.append(application.morpheme_common.sharing_text_noun(line))

    with codecs.open("nanao_input_data2.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

#create_novel(file_open("ningen_shikkaku_syuki2.txt"))
#create_tweet(file_open("tweet.txt"))

collection_talk_million()
#collection_talk_theater()
#create_talk(file_open("nanao_data2.txt"))

def meidai_corps(fname,data2) :
    f = open(fname, 'r', encoding="utf-8_sig")
    df1 = csv.reader(f)
    data1 = [ v for v in df1]

    print(len(data1))
    #ファイル読み込み
    text = ''
    for i in range(0,len(data1)):
        if len(data1[i]) == 0:
            print('null')
            continue

        s = data1[i][0]
        if s[0:5] == "％ｃｏｍ：" :
            continue
        if s[0]  != '＠' :
            #不明文字をUNKに置き換え
            s = s.replace('＊＊＊','UNK')
            #会話文セパレータ
            if s[0] == 'F' or s[0] == 'M':
                s = 'SSSS'+s[5:]
            if s[0:2] == 'Ｘ：':
                s = 'SSSS'+s[2:]

            s = re.sub('F[0-9]{3}',"UNK",s)
            s = re.sub('M[0-9]{3}',"UNK",s)
            s = s.replace("＊","")
        else :
            continue

        while s.find("（") != -1 :
            start_1 = s.find("（")
            if s.find("）") != -1 :
                end_1 = s.find("）")
                if start_1 >= end_1 :
                    s = s.replace(s[end_1],"")
                else :
                    s = s.replace(s[start_1:end_1+1],"")
                if len(s) == 0 :
                    continue
            else :
                s=s[0:start_1]

        while s.find("［") != -1 :
            start_2 = s.find("［")
            if s.find("］") != -1 :
                end_2=s.find("］")
                s=s.replace(s[start_2:end_2+1],"")
            else :
                s=s[0:start_2]

        while s.find("＜") != -1 :
            start_3 = s.find("＜")
            if s.find("＞") != -1 :
                end_3 = s.find("＞")
                s = s.replace(s[start_3:end_3+1],"")
            else :
                s = s[0:start_3]

        while s.find("【") != -1 :
            start_4 = s.find("【")
            if s.find("】") != -1 :
                end_4 = s.find("】")
                s = s.replace(s[start_4:end_4+1],"")
            else :
                s = s[0:start_4]

        #いろいろ削除したあとに文字が残っていたら出力文字列に追加
        if s != "\n" and s != "SSSS" :
            text += s
    #セパレータごとにファイル書き込み
    text =text[4:]
    while text.find("SSSS") != -1 :
        end_s = text.find("SSSS")
        t = text[0:end_s]
        #長い会話文を分割
        if end_s > 100 :
            while len(t) > 100 :
                if t.find("。") != -1 :
                    n_period = t.find("。")
                    data2.append(t[0:n_period+1])
                    t = t[n_period+1:]
                else :
                    break
        data2.append(t)
        text = text[end_s+4:]
    f.close()
    return

def make_corps():

    data2 = []
    meidai_corps("all.txt", data2)

    # ファイルセーブ
    f = open('corpus.txt', 'w',  encoding="utf-8_sig")
    for i in range(0, len(data2)):
        f.write(str(data2[i] + "\n"))
    f.close()
    print(len(data2))

def make_talk_meidai(lines):
    corps = []
    for line in lines:
        corps.append(application.morpheme_common.sharing_text_noun(line))

    with codecs.open("create_corpus.txt", "w", "utf-8") as f:
        f.write("\n".join(corps))

#make_corps()
#make_talk_meidai(file_open("corpus.txt"))