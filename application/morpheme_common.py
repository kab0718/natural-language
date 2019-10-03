import MeCab

def split_text(text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]      #featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        if hinsi != "記号":
            words.append(word)
        node = node.next    #次のnodeに移る

    word = ' '.join(words)

    return word

def sharing_text_noun(text):
    tagger = MeCab.Tagger("-Owakati -d C:\mecab-ipadic-neologd")

    tagger.parse("")    #エラー回避のために空文字をパース
    node = tagger.parseToNode(text)     #最初のnodeを取得

    words = []

    while node:
        word = node.surface     #surfaceには単語が入っている
        words.append(word)
        node = node.next    #次のnodeに移る

    return words    #名詞だけのリストを返す
