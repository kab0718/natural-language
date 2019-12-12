import application.morpheme_common
import pprint
import random
import re
import markovify

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

if __name__ == '__main__':
    contents = file_open('serif/kitazawa_serif.txt')    #contentsはテキストファイルの一行が一要素となったリスト
    sentences = marking_text(contents)    #ひとまず文の先頭と最後に目印となる*を付与。余裕あれば一文じゃなくて。で区切る
    corps = analysis(sentences)    #corpsは文章を形態素解析したもの
    blocks = generate_block(corps)    #blocksは品詞ごとに分解したものを三単語ごとのブロックに分けてあるリスト
    dict = generate_dictionary(blocks)
    for i in range(10):
        generate_text(dict)
