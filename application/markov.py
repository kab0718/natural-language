import application.morpheme_common

def file_open(file_name):
    test_data = open(file_name, encoding="utf_8_sig")

    contents = test_data.readlines()
    test_data.close()

    return contents

def analysis(contents):
    corps = []
    for content in contents:
        corps.append(application.morpheme_common.sharing_text_noun(content))

    return corps

if __name__ == '__main__':
    contents = file_open('serif/kitazawa_data.txt')    #contentsはテキストファイルの一行が一要素となったリスト
    corps = analysis(contents)    #corpsは文章を形態素解析したもの
