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
        for i in range(len(list)-1):
            block = list[i:i+2]    #2単語ずつのブロック作成
            blocks.append(block)
    return blocks

def generate_dictionary(blocks):
    dict = {}
    for block in blocks:
        pre_word = block[0]
        if pre_word in dict:
            list = dict[pre_word]
        else:
            list = []
        if block[-1] not in list:
            list.append(block[-1])
        dict[pre_word] = list

    return dict

def generate_text(blocks):
    top_blocks = []
    now_blocks = []

    for block in blocks:
        if(block[0] == '*'):
            top_blocks.append(block)
    sentences_top = top_blocks[random.randint(0, len(top_blocks) - 1)]
    sentence = ''.join(sentences_top)

    while sentence[-1] != '*':
        block_last = sentence[-1]
        for block in blocks:
            if(block[0] == block_last):
                now_blocks.append(block)
        if not now_blocks:
            break
        add_block = now_blocks[random.randint(0, len(now_blocks) - 1)]
        sentence = sentence + ''.join(add_block[1:])
    print(sentence)


if __name__ == '__main__':
    contents = file_open('serif/sihosizu.txt')    #contentsはテキストファイルの一行が一要素となったリスト
    sentences = marking_text(contents)    #ひとまず文の先頭と最後に目印となる*を付与。余裕あれば一文じゃなくて。で区切る
    corps = analysis(sentences)    #corpsは文章を形態素解析したもの
    blocks = generate_block(corps)    #blocksは品詞ごとに分解したものを三単語ごとのブロックに分けてあるリスト
    dict = generate_dictionary(blocks)