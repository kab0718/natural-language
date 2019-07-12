import MeCab
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def sharing_text(text):
    tagger = MeCab.Tagger("-Owakati -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        words.append(word)
        node = node.next    #次のnodeに移る

    return words    #名詞だけのリストを返す

text = "令和元年硬貨と天皇陛下即位の記念硬貨の打ち初め式が、大阪市北区の造幣局で行われました"
wakati_text = ' '.join(sharing_text(text))    #リストを半角スペースごとに結合
print(wakati_text)

message_list = [
    ' '.join(sharing_text("私達はラーメンがとても大好きです。")),
    ' '.join(sharing_text("私達は蕎麦がとても大好きです。"))
]

docs = np.array(message_list)

count = CountVectorizer()
bags = count.fit_transform(docs)

print(bags.toarray())   #特徴量ベクトルに変換したものを出力

features = count.get_feature_names()
print(features)
