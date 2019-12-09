import application.morpheme_common

def file_open(file_name):
    test_data = open(file_name, encoding="utf_8_sig")

    contents = test_data.readlines()
    test_data.close()

    return contents

def marking_text(contents):
    sentences = []
    for content in contents:
        sentence = '* ' + content + ' *'
        sentences.append(sentence)
    return sentences

def analysis(contents):
    corps = []
    for content in contents:
        corps.append(application.morpheme_common.sharing_text_noun(content))

    return corps

def generate_block(corps):
    blocks = []
    for corp in corps:
        list = corp.split()
        for i in range(len(list)-3):
            block = list[i:i+3]
            blocks.append(block)
    return blocks

if __name__ == '__main__':
    contents = file_open('serif/kitazawa_data.txt')    #contentsはテキストファイルの一行が一要素となったリスト
    sentences = marking_text(contents)    #ひとまず文の先頭と最後に目印となる*を付与。余裕あれば一文じゃなくて。で区切る
    corps = analysis(sentences)    #corpsは文章を形態素解析したもの
    blocks = generate_block(corps)    #blocksは品詞ごとに分解したものを三単語ごとのブロックに分けてあるリスト
    print(blocks)
