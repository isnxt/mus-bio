import re


def format_sent(sentence):
    sentence = re.sub('《.*?》', '《作品》', sentence)
    sentence = re.sub('“.*?”', '“引号”', sentence)
    sentence = re.sub('《.*?》', '《作品》', sentence)
    return sentence


def convert_ners(ners):
    list_ners = []
    for ner in ners:
        list_ners.append(list(ner))
    return list_ners


def get_DATE(ners):
    list_date = []
    for i in range(len(ners)):
        word = ners[i][0]
        if word == '当时' or word == '现在' or word == '后来':
            ners[i][1] = 'O'
        tag = ners[i][1]
        if tag == 'DATE' and ners[i - 1][1] == 'DATE':
            pop_word = list_date.pop()
            list_date.append(pop_word + word)
        elif (word == '岁' or word == '岁时') and ners[i - 1][1] == 'NUMBER':
            list_date.append(ners[i - 1][0] + '岁')
        elif (word == '至' or word == '到') and ners[i - 1][1] == 'DATE' and ners[i + 1][1] == 'DATE':
            ners[i][1] = 'DATE'
            pop_word = list_date.pop()
            list_date.append(pop_word + '至')
        elif tag == 'DATE':
            list_date.append(word)
    set_date = sorted(set(list_date), key=list_date.index)
    if len(set_date) != 0:
        print('DATE:', set_date)
    return set_date


def get_PER(ners):
    list_per = []
    for i in range(len(ners)):
        word = ners[i][0]
        if "·" in ners[i-1][0] and word.encode('UTF-8').isalpha():
            ners[i][1] = 'PERSON'
        elif "·" in word:
            ners[i][1] = 'PERSON'
        tag = ners[i][1]
        if tag == 'PERSON' and ners[i - 1][1] == 'PERSON':
            pop_word = list_per.pop()
            list_per.append(pop_word + word)
        elif tag == 'PERSON':
            list_per.append(word)
    set_per = sorted(set(list_per), key=list_per.index)
    if len(set_per) != 0:
        print('PER:', set_per)

    return set_per


def get_LOC(ners):
    list_loc = []
    for i in range(len(ners)):
        word = ners[i][0]
        tag = ners[i][1]
        if tag == 'CITY' or tag == 'COUNTRY' or tag == 'LOCATION':
            list_loc.append(word)
    set_loc = sorted(set(list_loc), key=list_loc.index)
    if len(set_loc) != 0:
        print('LOC:', set_loc)
    return set_loc
def get_GPE(ners):
    list_gpe = []
    for i in range(len(ners)):
        word = ners[i][0]
        tag = ners[i][1]
        if tag == 'GPE':
            list_gpe.append(word)
    set_gpe = sorted(set(list_gpe), key=list_gpe.index)
    print('\nGPE:', set_gpe)
    return set_gpe

def get_word(ners):
    ners = convert_ners(ners)
    list_per = get_PER(ners)
    list_location = get_LOC(ners)
    list_date = get_DATE(ners)
    # list_GPE = get_GPE(ners)
    return list_date, list_per, list_location


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    para = para.split("\n")
    return para


if __name__ == "__main__":
    format_sent("我于1998年")
