import application.morpheme_common
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def text_import(file_name):
    text = open(file_name, encoding="utf_8_sig").read()
    lines = text.split("\n")
    return lines

def sharing(lines):
    req_list = []
    res_list = []
    for line in lines:
        if "REQ:" in line:
            line = line.split(":")[1] #REQ:を削除
            req_list.append(application.morpheme_common.split_text(line))
        elif "RES:" in line:
            line = line.split(":")[1] #RES:を削除
            res_list.append(application.morpheme_common.split_text(line))
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

def both_get_tag(lines):
    both_list = []
    tag_both_list = []
    req_id = 1
    res_id = 1
    for line in lines:
        line = line.split(":")[1]
        both_list.append(application.morpheme_common.split_text(line))
    for i,list in enumerate(both_list, start=1):
        if i % 2 == 1:
            both = TaggedDocument(words=list, tags=["REQ" + str(req_id)])
            req_id += 1
        else:
            both = TaggedDocument(words=list, tags=["RES" + str(res_id)])
            res_id += 1
        tag_both_list.append(both)

    return tag_both_list

lines = text_import("tweet.txt") #テキストファイル読み込み

tag_both_list = both_get_tag(lines)

req_list, res_list = sharing(lines) #req_list[0]とres_list[0]が対応している
tag_req_list , tag_res_list = get_tag(req_list, res_list)

'''
req_model = Doc2Vec(documents=tag_req_list, vector_size=100, alpha=0.0015, window=10, min_count=1, workers=4)
req_model.save("req.model")

res_model = Doc2Vec(documents=tag_res_list, vector_size=100, alpha=0.0015, window=10, min_count=1, workers=4)
res_model.save("res.model")

both_model = Doc2Vec(documents=tag_both_list, vector_size=200, alpha=0.015, window=18, mincount=1, workers=8, epochs=10)
both_model.save("both.model")
'''
