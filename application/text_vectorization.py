import MeCab
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def text_import(file_name):
    text = open(file_name, encoding="utf_8_sig").read()
    lines = text.split("\n")
    return lines

def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]      #featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        if hinsi == "名詞" or "動詞" or "形容詞":
            words.append(word)
        node = node.next    #次のnodeに移る

    word = ' '.join(words)

    return word

def sharing(lines):
    req_list = []
    res_list = []
    for line in lines:
        if "REQ:" in line:
            line = line.split(":")[1] #REQ:を削除
            req_list.append(split_text_noun(line))
        elif "RES:" in line:
            line = line.split(":")[1] #RES:を削除
            res_list.append(split_text_noun(line))
    return req_list, res_list

def get_tag(req_list, res_list):
    tag_req_list = []
    tag_res_list = []
    req_id = 1
    res_id = 1
    for list in req_list:
        req = TaggedDocument(words=list, tags=['REQ' + str(req_id)]) #Doc2Vecで学習させるためのタグ付け
        tag_req_list.append(req)
        req_id += 1
    for list in res_list:
        res = TaggedDocument(words=list, tags=['RES' + str(res_id)])
        tag_res_list.append(res)
        res_id += 1

    return tag_req_list, tag_res_list

lines = text_import("tweet.txt") #テキストファイル読み込み
req_list, res_list = sharing(lines) #req_list[0]とres_list[0が対応している

tag_req_list , tag_res_list = get_tag(req_list, res_list)

req_model = Doc2Vec(documents=tag_req_list, vector_size=500, alpha=0.015, window=10, min_count=1, workers=4)
res_model = Doc2Vec(documents=tag_res_list, vector_size=500, alpha=0.015, window=10, min_count=1, workers=4)

req_model.save("req.model")
res_model.save("res.model")

req = Doc2Vec.load("req.model")
res = Doc2Vec.load("res.model")

print(res.docvecs.most_similar(0))