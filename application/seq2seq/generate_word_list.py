def create_list(filename):
    f = open(filename, encoding="utf-8_sig")
    lines = f.readlines()
    f.close()
    word_list = []
    for line in lines:
      for li in line:
        word_list.append(li)

    return word_list

word_list = create_list("create_corpus.txt")