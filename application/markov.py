import application.morpheme_common
import pprint
import random
import re
import MeCab

def file_open(file_name):
    test_data = open(file_name, encoding="utf_8_sig")

    contents = test_data.readlines()
    test_data.close()

    return contents

def marking_text(contents):
    sentences = []
    delete = []
    for content in contents:
        content = content.strip('\n')
        delete.append(content)
    content = ''.join(delete)    #区切るために一旦リストを一行の文にしている
    contents = re.findall('.*?[。|？|！]', content)    #。,！,？ごとに分割したリスト生成
    contents = [con for con in contents if con != '']    #空リストを取り除く

    for content in contents:
        sentence = '* ' + content + ' *'    #開始と終了の目印
        sentences.append(sentence)

    return sentences

def analysis(contents):
    corps = []
    for content in contents:
        corps.append(application.morpheme_common.sharing_text_noun(content))    #形態素解析

    return corps

def generate_block(corps):
    blocks = []
    for corp in corps:
        list = corp.split()
        for i in range(len(list)-2):
            block = list[i:i+3]    #3単語ずつのブロック作成
            blocks.append(block)
    return blocks

def generate_dictionary(blocks):
    dict = {}
    for block in blocks:
        if (block[0], block[1]) in dict:
            list = dict[(block[0], block[1])]
        else:
            list = []
        list.append(block[-1])
        dict[(block[0], block[1])] = list

    return dict

def generate_text(dict):
    while True:
        key1, key2 = random.choice(list(dict.keys()))
        if key1 == '*' : break;
    text = key2

    while True:
        word = random.choice(dict[(key1, key2)])
        if word == '*': break
        text += word
        key1, key2 = key2, word
    print(text)

def return_text(input_text):
    noun = create_noun_list(input_text)

def create_noun_list(input_text):
    tagger = MeCab.Tagger("-Ochasen -d C:\mecab-ipadic-neologd")
    node = tagger.parseToNode(input_text)  # 最初のnodeを取得

    nouns = []
    noun = None

    while node:
        word = node.surface  # surfaceには単語が入っている
        hinsi = node.feature.split(",")[0]  # featureには品詞や品詞細分類,活用形,読み方など様々な情報が入っている
        hinsi_detail = node.feature.split(",")[1]

        if hinsi == "名詞" and (hinsi_detail == '一般' or hinsi_detail == '固有名詞'):
            nouns.append(word)
        node = node.next  # 次のnodeに移る)
    print(nouns)
    if len(nouns) != 0:
        noun = random.choice(nouns)

    return noun

if __name__ == '__main__':
    contents = file_open('tweet.txt')    #contentsはテキストファイルの一行が一要素となったリスト
    sentences = marking_text(contents)    #ひとまず文の先頭と最後に目印となる*を付与。余裕あれば一文じゃなくて。で区切る
    corps = analysis(sentences)    #corpsは文章を形態素解析したもの
    blocks = generate_block(corps)    #blocksは品詞ごとに分解したものを三単語ごとのブロックに分けてあるリスト
    dict = generate_dictionary(blocks)
    for i in range(20):
        generate_text(dict)

    #input_text = '偽として評価されるものは他にもあるので注意してください'
    #return_text(input_text)