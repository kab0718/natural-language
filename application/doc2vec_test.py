import application.morpheme_common
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def main():
    req = Doc2Vec.load("req.model")
    res = Doc2Vec.load("res.model")
    both = Doc2Vec.load("both.model")

    print(both.docvecs.most_similar(0)) #both.modelの中でreq1と類似度が高い10件を表示

    print(both.docvecs["REQ1"]) #REQ1のベクトルを表示
    print(both.docvecs.similarity("REQ1","RES1")) #REQ1とRES1の類似度表示

    input_text = """バーレーンの首都マナマ(マナーマとも)で現在開催されている
    ユネスコ(国際連合教育科学文化機関)の第42回世界遺産委員会は日本の推薦していた
    「長崎と天草地方の潜伏キリシタン関連遺産」 (長崎県、熊本県)を30日、
    世界遺産に登録することを決定した。"""

    pro_text = application.morpheme_common.split_text(input_text).split()
    vec_input = both.infer_vector(pro_text)
    print(vec_input) #入力テキストをベクトル化したものを出力

    input_similar = both.docvecs.most_similar([vec_input],topn=100)

    input_similar_req = []
    count = 0

    while len(input_similar_req) != 5:
        if "REQ" in input_similar[count][0]:    # input_similarの各要素はtupleになっている
            input_similar_req.append(input_similar[count])
        else:
            pass
        count += 1
    print(input_similar_req)
    req_tag = input_similar_req[0][0]
    res_tag = req_tag.replace("REQ", "RES")
    print(res_tag)
    print(both.docvecs[res_tag])

if __name__ == "__main__":
    main()
