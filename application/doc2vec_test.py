import application.morpheme_common
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def main():
    both = Doc2Vec.load("both.model")

    print(both.docvecs.most_similar(0)) #both.modelの中でreq1と類似度が高い10件を表示

    print(both.docvecs["REQ1"]) #REQ1のベクトルを表示
    print(both.docvecs.similarity("REQ1","RES1")) #REQ1とRES1の類似度表示

    input_text = "いつかインスタのオシャレな写真の中にこってり系ラーメンを紛れ込ませて人々の胃袋を刺激したい。"

    pro_text = application.morpheme_common.split_text(input_text).split()
    vec_input = both.infer_vector(pro_text)
    print(vec_input) #入力テキストをベクトル化したものを出力

    input_similar = both.docvecs.most_similar([vec_input],topn=100)

    input_similar_req = []
    count = 0

    while len(input_similar_req) != 5: #入力文章に近いベクトル上位5件を求めてる
        if "REQ" in input_similar[count][0]:    # input_similarの各要素はtupleになっている
            input_similar_req.append(input_similar[count])
        else:
            pass
        count += 1
    print(input_similar_req)
    req_tag = input_similar_req[0][0] #入力文章ベクトルに一番近い入力データのタグ
    res_tag = req_tag.replace("REQ", "RES") #入力文章ベクトルに一番近い入力データへの返答のタグ
    print(res_tag)
    print(both.docvecs[res_tag]) #入力文章に一番近い入力データへの返答

if __name__ == "__main__":
    main()
