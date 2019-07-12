import MeCab

def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")
    node = tagger.parseToNode(text)

    while node:
        word = node.surface
        hinsi = node.feature.split(",")[0]
        if hinsi == "名詞":
            print(word + ":" + hinsi)
        node = node.next

text = "私はラーメンが好きです"
split_text_noun(text)