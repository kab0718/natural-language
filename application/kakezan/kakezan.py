import re
import MeCab
import codecs
import sys
import random
import matplotlib
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup
from gensim.models import word2vec
from wordcloud import WordCloud


def file_open(file_name):
    test_data = open(file_name, "r", encoding="utf-8_sig")

    contents = test_data.read()
    test_data.close()

    return contents


def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd\\build\mecab-ipadic-2.7.0-20070801-neologd-20190808")

    tagger.parse("")  # エラー回避のために空文字をパース
    node = tagger.parseToNode(text)  # 最初のnodeを取得

    words = []

    while node:
        word = node.surface  # surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]  # featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        if hinsi == "名詞":
            if re.search('[0-9]+', word):
                pass
            else:
                words.append(word)
        node = node.next  # 次のnodeに移る

    word = ' '.join(words)

    return word


def wordcloud(text):
    word = WordCloud(background_color="white", font_path="C:\Windows\Fonts\メイリオ", width=1024,
                          height=674).generate(text)

    word.to_file("./test.png")


tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd\\build\mecab-ipadic-2.7.0-20070801-neologd-20190808")
corps = []
'''
link = "https://dic.pixiv.net/a/"
keyword = ["望月杏奈", "七尾百合子", "天海春香", "春日未来", "如月千早", "木下ひなた", "四条貴音",
           "ジュリア", "高山紗代子", "田中琴葉", "天空橋朋花", "箱崎星梨花", "松田亜利沙", "三浦あずさ",
           "水瀬伊織", "最上静香", "矢吹可奈", "エミリー・スチュアート", "大神環", "我那覇響", "菊地真",
           "北上麗花", "高坂海美", "佐竹美奈子", "島原エレナ", "高槻やよい", "永吉昴", "野々原茜", "馬場このみ",
           "福田のり子", "舞浜歩", "真壁瑞希", "百瀬莉緒", "横山奈緒", "秋月律子", "伊吹翼", "北沢志保",
           "篠宮可憐", "周防桃子", "徳川まつり", "所恵美", "豊川風花", "中谷育", "二階堂千鶴", "萩原雪歩",
           "双海亜美", "双海真美", "星井美希", "宮尾美也", "伴田路子", "白石紬", "桜守歌織", "はるみら", "あんゆり",
           "みななお", "いくもも", "かおつむ", "ことエレ", "ことめぐ", "しずしほ", "みきつば", "みらしず", "かなしほ",
           "はるみら", "あんゆり", "ちはしず", "みずもも", "シアターデイズ", "ミリオンライブユニット",
           "レジェンドデイズ", "乙女ストーム!", "クレシェンドブルー", "エターナルハーモニー",
           "灼熱少女", "ミックスナッツ", "ARRIVE", "フェアリースターズ", "エンジェルスターズ", "プリンセススターズ", "Cleasky",
           "トゥインクルリズム", "EScape", "4Luxury", "閃光☆HANABI団",
           "りるきゃん", "Charlotte・Charlotte", "ピコピコプラネッツ", "ミリラジ組", "トライスタービジョン", "ミリマス15歳組"]

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
corps.append((file_open("pixiv_wiki.txt")))

# corpsのそれぞれの要素の末尾に改行文字追加
with codecs.open("pixiv_wiki.txt", "w", "utf-8") as f:
    f.write("\n".join(corps))

with codecs.open("pixiv_wiki.txt", "r", "utf-8") as f:
    corps = f.read().splitlines()

corps = [sentence.split() for sentence in corps]
# モデル作成
model = word2vec.Word2Vec(corps, size=30, min_count=13, window=8, iter=100)
# モデル保存
model.save("pixiv_wiki.model")
# モデル読みこみ
model = word2vec.Word2Vec.load("pixiv_wiki.model")

seme = sys.argv[1]
uke = sys.argv[2]
key = "百合"
#単語のベクトルを見る
word_vector = model.wv[key]
print(word_vector)
#keyに入った単語と類似単語を見る
#similar_words = model.wv.most_similar(positive=[key], topn=10)
#print(*[" ".join([v, str("{:.2f}".format(s))]) for v, s in similar_words], sep="\n") #similar_wordsはリストになっていて要素は単語と類似度の組になっている
words = model.most_similar([word_vector], [], 15000)
print(words)

for name, vector in words:
    if(seme == name):
        seme_vec = abs(vector * 10)
    elif(uke == name):
        uke_vec = abs(vector)

result = seme_vec * uke_vec
print(seme_vec)
print(uke_vec)
print(result)