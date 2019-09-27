import application.morpheme_common
import numpy as np
import pandas as pd
import openpyxl
import pprint
from gensim.models import word2vec
import gensim
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

np.set_printoptions(threshold=np.inf)

def file_open(file_name):
    test_data = open(file_name, "r")

    contents = test_data.read()
    test_data.close()

    return contents

message_list = [
    #' '.join(split_text_noun("高専や理系の勉強，ものづくりに興味はありませんか？函館高専では，『一日高専生』を体験できる「オープンキャンパス」を開催します。")),
    #' '.join(split_text_noun("高専でどのような勉強をしているか，体験して自分の目で確かめられるチャンスです")),
    #' '.join(split_text_noun(file_open("sanshiro.txt"))),
    ' '.join(application.morpheme_common.sharing_text_noun(file_open("ningen_shikkaku_syuki2.txt")))
]

#抽出した名詞からベクトルを得る
docs = np.array(message_list)   #メッセージリストをndarrayを呼ばれる型付き高次元配列に変換

count = CountVectorizer()   #CountVectorizerをインスタンス化
bags = count.fit_transform(docs)
# fitで変換式を計算する(データを変換するのに必要な統計情報の計算)
# transformではfitの結果を使って実際にデータを変換する
# fit_tranceformはfitとtranceformをまとめて行っている
# https://mathwords.net/fittransform 参照

bags_array = []
for b in bags.toarray():
    for bag in b:
        bags_array.append(bag)

print(bags_array)   #特徴量ベクトルに変換したものを出力


features = count.get_feature_names()    #ベクトルに変換した単語をリスト化
print(features)

tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)  #TfidfTransformerでtf-idfを計算してくれる
#TfidfTransformerの仕様については https://akamist.com/blog/archives/2849 参照
np.set_printoptions(precision=2)    #有効数字二桁に設定
tf_idf = tfidf.fit_transform(bags)

tf_idf_array = []
for tf in tf_idf.toarray():
    for idf in tf:
        tf_idf_array.append(round(idf, 5))

print(tf_idf_array)     #出てきた値を配列にして出力


'''
df = pd.DataFrame([features, bags_array, tf_idf_array])

df.to_excel('data3.xlsx',sheet_name='sanshiro')
'''