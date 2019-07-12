import MeCab
import numpy
from sklearn.feature_extraction.text import CountVectorizer

def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]      #featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        if hinsi == "名詞":
            words.append(word)
        node = node.next    #次のnodeに移る

    return words    #名詞だけのリストを返す

text = "令和元年硬貨と天皇陛下即位の記念硬貨の打ち初め式が、大阪市北区の造幣局で行われました"
split_text = ' '.join(split_text_noun(text))    #リストを半角スペースごとに結合
print(split_text)