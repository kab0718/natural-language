import MeCab
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

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

message_list = [
    ' '.join(split_text_noun("高専や理系の勉強，ものづくりに興味はありませんか？函館高専では，『一日高専生』を体験できる「オープンキャンパス」を開催します。")),
    ' '.join(split_text_noun("高専でどのような勉強をしているか，体験して自分の目で確かめられるチャンスです"))
]

#抽出した名詞からベクトルを得る
docs = np.array(message_list)   #メッセージリストをndarrayを呼ばれる型付き高次元配列に変換

count = CountVectorizer()   #CountVectorizerをインスタンス化
bags = count.fit_transform(docs)
# fitで変換式を計算する(データを変換するのに必要な統計情報の計算)
# transformではfitの結果を使って実際にデータを変換する
# fit_tranceformはfitとtranceformをまとめて行っている
# https://mathwords.net/fittransform 参照

print(bags.toarray())   #特徴量ベクトルに変換したものを出力

features = count.get_feature_names()    #ベクトルに変換した単語をリスト化
print(features)

tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)  #TfidfTransformerでtf-idfを計算してくれる
#TfidfTransformerの仕様については https://akamist.com/blog/archives/2849 参照
np.set_printoptions(precision=2)    #有効数字二桁に設定
tf_idf = tfidf.fit_transform(bags)
print(tf_idf.toarray())     #出てきた値を配列にして出力