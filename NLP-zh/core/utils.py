import re
import zhconv
import os
import sys
import shutil
import requests

root_path = os.path.abspath('.')


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""

    if uchar >= u'/u4e00' and uchar <= u'/u9fa5':

        return True

    else:

        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""

    if uchar >= u'/u0030' and uchar <= u'/u0039':

        return True

    else:

        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""

    if (uchar >= u'/u0041' and uchar <= u'/u005a') or (uchar >= u'/u0061' and uchar <= u'/u007a'):

        return True

    else:

        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""

    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):

        return True

    else:

        return False


def clean_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def del_bracket(str_data):
    int_symbol = 0
    str_data2 = ""
    set_symbol = {('（', '）')}
    for c in str_data:
        if c in [tuple_symbol[0] for tuple_symbol in set_symbol]:
            int_symbol += 1
            if int_symbol == 1:
                continue
        elif c in [tuple_symbol[1] for tuple_symbol in set_symbol]:
            int_symbol -= 1
            if int_symbol == 0:
                str_symbol = ""
                continue
        if int_symbol == 0:
            str_data2 += c
    return str_data2


def add_space(str_data):
    # 在前加空格
    set_mat_front = set(re.findall(r"(于\d{2,4}年|在\d{2,4}年)", str_data))
    if len(set_mat_front) != 0:
        for item in set_mat_front:
            str_data = str_data.replace(item, " " + item)
    # 在后加空格
    set_mat_back = set(re.findall(r"(因此)", str_data))
    if len(set_mat_back) != 0:
        for item in set_mat_back:
            str_data = str_data.replace(item, item + " ")
    return str_data


def del_blank(str_data):
    str_data = str_data.replace('\xa0', ' ')
    str_data2 = ''
    for i in range(len(str_data)):
        if str_data[i] == ' ' and str_data[i - 1].encode('UTF-8').isalpha() and str_data[i + 1].encode(
                'UTF-8').isalpha():
            str_data2 += ' '
            continue
        elif str_data[i] == ' ':
            continue
        str_data2 += str_data[i]
    return str_data2


def th2zh(str_data):
    if str_data is None:
        return str_data
    else:
        return zhconv.convert(str_data, 'zh-cn')


def format_data(str_data):
    # 标准化字符
    str_data = sbc2dbc(str_data)
    str_data = str_data.replace('。”', '。”\n')
    # 去空格
    # str_data = del_blank(str_data)
    # 去括号
    str_data = del_bracket(str_data)
    # 将繁体转换成简体
    str_data = th2zh(str_data)
    # 加空格
    # str_data = add_space(str_data)
    return str_data


def short_data(sentence):
    int_symbol = 0
    sentence2 = ""
    str_symbol = ""
    list_symbol = []
    set_symbol = {('《', '》'), ('“', '”'), ('｢', '｣'), ('[', ']')}
    for c in sentence:
        if c in [tuple_symbol[0] for tuple_symbol in set_symbol]:
            int_symbol += 1
            if int_symbol == 1:
                sentence2 += c + "简化"
                str_symbol += c
                continue
        elif c in [tuple_symbol[1] for tuple_symbol in set_symbol]:
            int_symbol -= 1
            if int_symbol == 0:
                sentence2 += c
                str_symbol += c
                list_symbol.append(str_symbol)
                str_symbol = ""
                continue
        if int_symbol != 0:
            str_symbol += c
        if int_symbol == 0:
            sentence2 += c
    return sentence2, list_symbol


def long_data(para, list_symbol):
    if len(list_symbol) > 0:
        list_symbol.reverse()
        rev_list_symbol = list_symbol
        for i in range(len(para)):
            j = 0
            int_length = len(para[i])
            while j + 3 < int_length and len(rev_list_symbol) != 0:
                if para[i][j] == rev_list_symbol[-1][0] and para[i][j + 3] == rev_list_symbol[-1][-1]:
                    str_add = rev_list_symbol.pop()[1:-1]
                    para[i] = para[i][0:j + 1] + str_add + para[i][j + 3:]
                    j += len(str_add) + 1
                    int_length = len(para[i])

                else:
                    j += 1

    return para


def long_ners(ners, list_symbol):
    if len(list_symbol) > 0:
        list_symbol.reverse()
        rev_list_symbol = list_symbol
        for i in range(len(ners)):
            if i + 2 < len(ners) and len(list_symbol) != 0:
                if ners[i][0] == list_symbol[-1][0] and ners[i + 2][0] == list_symbol[-1][-1]:
                    ners[i + 1][0] = rev_list_symbol.pop()[1:-1]
    return ners


def age2year(birth, death, sent):
    year = re.findall('(\d{4}年)', sent)
    if len(year) == 0:
        ages = re.findall('(\d+岁)', sent)
        for i in range(len(ages)):
            age = int(ages[i][:-1])
            if len(birth) >= 4:
                sent = sent.replace(ages[i], str(int(birth[:4]) + age) + "年")
            elif len(death) >= 4:
                sent = sent.replace(ages[i], str(int(death[:4]) - age) + "年")
    return sent



def drop_dup(ids):
    new_ids = []
    for id in ids:
        if id not in new_ids:
            new_ids.append(id)
    return new_ids


def cut_sent(para):
    para, list_symbol = short_data(para)
    para = re.sub('([。！？；\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.rstrip()
    para = para.split('\n')
    # 还原
    para = long_data(para, list_symbol)
    return para


def sbc2dbc(str_data):
    # 半角转全角
    list_char = [('【', '['), ('】', ']'), ('｢', '“'), ('｣', "”"), (',', '，'), ('?', '？'), ('!', '！'), ('(', '（'),
                 (')', '）'), (':', '：'), ('-', '-'),('—','-')]
    for i in range(len(list_char)):
        str_data = str_data.replace(list_char[i][0], list_char[i][1])
    return str_data


def zh2number(str_phrase):
    # constants for chinese_to_arabic
    all_zh = re.findall('[一二两三四五六七八九零十百千万亿]+', str_phrase)
    map_num = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
               '百': 100, '千': 1000, '万': 10000, '亿': 100000000}

    for str_zh in all_zh:
        str_num = ""
        if not bool(set('十百千万亿').intersection(str_zh)):
            for i in range(len(str_zh)):
                val = map_num.get(str_zh[i])
                str_num += str(val)
        else:
            total = 0
            r = 1  # 表示单位：个十百千...
            for i in range(len(str_zh) - 1, -1, -1):
                val = map_num.get(str_zh[i])
                if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                    if val > r:
                        r = val
                        total = total + val
                    else:
                        r = r * val
                        # total =total + r * x
                elif val >= 10:
                    if val > r:
                        r = val
                    else:
                        r = r * val
                else:
                    total = total + r * val
            str_num = str(total)
        str_phrase = str_phrase.replace(str_zh, str_num, 1)
    return str_phrase


if __name__ == "__main__":
    zh2number("二")

