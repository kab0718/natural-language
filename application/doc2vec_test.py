import MeCab
from gensim.models.doc2vec import Doc2Vec

req = Doc2Vec.load("req.model")
res = Doc2Vec.load("res.model")
both = Doc2Vec.load("both.model")

print(res.docvecs.most_similar(0)) #req.modelの中でres1と類似度が高い10件を表示
print(req.docvecs.most_similar(0))
print(both.docvecs.most_similar(0))

print(both.docvecs["REQ1"]) #REQ1のベクトルを表示
print(both.docvecs.similarity("REQ1","RES1")) #REQ1とRES1の類似度表示

