import application.morpheme_common
import numpy as np
import MeCab
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def sharing_text(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd\\build\mecab-ipadic-2.7.0-20070801-neologd-20190808")

def main():
    message_list = [
        ' '.join(application.morpheme_common.sharing_text_noun("高専や理系の勉強，ものづくりに興味はありませんか？函館高専では，『一日高専生』を体験できる「オープンキャンパス」を開催します。")),
        ' '.join(application.morpheme_common.sharing_text_noun("高専でどのような勉強をしているか，体験して自分の目で確かめられるチャンスです"))
    ]


    docs = np.array(message_list)

    count = CountVectorizer()
    bags = count.fit_transform(docs)


    while node:
        word = node     #surfaceには単語が入っている
        words.append(word)
        node = node.next    #次のnodeに移る

    print(bags.toarray())   #特徴量ベクトルに変換したものを出力


    features = count.get_feature_names()
    print(features)

    tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
    np.set_printoptions(precision=2)
    tf_idf = tfidf.fit_transform(bags)
    print(tf_idf.toarray())

if __name__ == "__main__":
    main()