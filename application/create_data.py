import application.morpheme_common
import re
import codecs

def file_open(file_name):
    test_data = open(file_name, encoding="utf_8_sig")

    contents = test_data.readlines()
    test_data.close()

    return contents

lines = file_open("ningen_shikkaku_syuki2.txt")
corps = []
for line in lines:
    text = line
    text = re.split(r'\r', text)[0]  # 改行削除
    text = text.replace('｜', '')  # ルビ前記号削除
    text = re.sub(r'《.+?》', '', text)  # ルビ削除
    text = re.sub(r'［＃.+?］', '', text)  # 入力者注削除
    corps.append(application.morpheme_common.split_text(text))
# corpsのそれぞれの要素の末尾に改行文字追加
with codecs.open("input_data.txt", "w", "utf-8") as f:
    f.write("\n".join(corps))


