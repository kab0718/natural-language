import re
import MeCab
import codecs
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup
from gensim.models import word2vec

def file_open(file_name):
    test_data = open(file_name, "r")

    contents = test_data.read()
    test_data.close()

    return contents

def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]      #featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        if hinsi == "名詞":
            if re.search('[0-9]+', word):
                pass
            else:
                words.append(word)
        node = node.next    #次のnodeに移る

    word = ' '.join(words)

    return word

tagger = MeCab.Tagger("-Owakati -d C:\mecab-ipadic-neologd")
corps = []
'''
link = "https://ja.wikipedia.org/wiki/"
keyword = ["伊藤美来", "夏川椎菜", "雨宮天",
           "麻倉もも", "田所あずさ", "種田梨沙",
           "豊田萌絵", "内田真礼", "阿澄佳奈",
           "駒形友梨", "上田麗奈", "小澤亜李",
           "大橋彩香", "戸松遥", "坂本真綾",
           "田村ゆかり", "中原麻衣", "名塚佳織"]
for word in keyword:
    with request.urlopen(link + parser.quote_plus(word)) as response:
        #responseはhtmlのformatになっている
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        #<p>タグを取得
        p_tags = soup.find_all('p')
        # html形式の文字列から<p></p>で囲まれている部分を取り出し形態素解析→corpsに追加
        for p in p_tags:
            corps.append(split_text_noun(p.text))
'''
corps.append(split_text_noun((file_open("ningen_shikkaku_syuki2.txt"))))

#corpsのそれぞれの要素の末尾に改行文字追加
with codecs.open("pwiki.txt", "w", "utf-8") as f:
    f.write("\n".join(corps))

with codecs.open("pwiki.txt", "r", "utf-8") as f:
    corps = f.read().splitlines()

corps = [sentence.split() for sentence in corps]
#モデル作成
model = word2vec.Word2Vec(corps, size=200, min_count=15, window=10)
#モデル保存
model.save("pwiki.model")
#モデル読みこみ
model = word2vec.Word2Vec.load("pwiki.model")

key = "自分"
#単語のベクトルを見る
word_vector = model.wv[key]
#keyに入った単語と類似単語を見る
similar_words = model.wv.most_similar(positive=[key], topn=9)
print(*[" ".join([v, str("{:.2f}".format(s))]) for v, s in similar_words], sep="\n") #similar_wordsはリストになっていて要素は単語と類似度の組になっている
