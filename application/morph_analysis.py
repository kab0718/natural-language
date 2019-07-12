import MeCab

def split_text_noun(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")
    node = tagger.parseToNode(text)

    words = []

    while node:
        word = node.surface
        hinsi = node.feature.split(",")[0]
        if hinsi == "名詞":
            words.append(word)
        node = node.next

    return words

text = "令和元年硬貨と天皇陛下即位の記念硬貨の打ち初め式が、大阪市北区の造幣局で行われました"
split_text = split_text_noun(text)
print(split_text)