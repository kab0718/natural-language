import application.morpheme_common
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def main():
    req = Doc2Vec.load("req.model")
    res = Doc2Vec.load("res.model")
    both = Doc2Vec.load("both.model")

    print(res.docvecs.most_similar(0)) #req.modelの中でres1と類似度が高い10件を表示
    print(req.docvecs.most_similar(0))
    print(both.docvecs.most_similar(0))

    print(both.docvecs["REQ1"]) #REQ1のベクトルを表示
    print(both.docvecs.similarity("REQ2","RES2")) #REQ1とRES1の類似度表示

    input_text = """バーレーンの首都マナマ(マナーマとも)で現在開催されている
    ユネスコ(国際連合教育科学文化機関)の第42回世界遺産委員会は日本の推薦していた
    「長崎と天草地方の潜伏キリシタン関連遺産」 (長崎県、熊本県)を30日、
    世界遺産に登録することを決定した。"""

    pro_text = application.morpheme_common.split_text(input_text).split()

    print(both.infer_vector(pro_text)) #入力テキストをベクトル化したものを出力
    print(both.docvecs.most_similar([both.infer_vector(pro_text)])) #入力テキストに最も近い10個を出力

if __name__ == "__main__":
    main()
