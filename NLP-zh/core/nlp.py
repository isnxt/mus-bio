import os
import re

from stanfordcorenlp import StanfordCoreNLP

from core import utils

root_path = os.path.abspath('.')


def analyse(para):
    print("\nanalyse...")
    para = utils.format_data(para)
    sentences = utils.cut_sent(para)
    para_ners = []
    nlp_model = NLP()
    nlp_model.set_birth(sentences)
    for sentence in sentences:
        if sentence != "":
            list_ners = nlp_model.ner(sentence)
            for ners in list_ners:
                dates, pers, locs, sentence = ners[0], ners[1], ners[2], ners[3]
                if len(dates) > 0:
                    para_ners.append([dates, pers, locs, sentence])
                    # print("----------------------------------------------------")
                    # if len(pers) != 0:
                    #     print('sentence:', sentence)
                    #     print(pers)
    nlp_model.close()
    return sorted(para_ners)


class NLP:
    def __init__(self):
        # Use an existing server
        self.nlp = StanfordCoreNLP('http://localhost',  port=9000, lang='zh')
        self.int_birth = 0
        self.last_year = ""
        self.last_month = ""
        self.props = {'annotators': 'ner', 'pipelineLanguage': 'zh', 'outputFormat': 'xml'}

    def close(self):
        self.nlp.close()

    def set_birth(self, sentences):
        # 提取出生时间
        set_birth = {'生于'}
        set_death = {'死于', '去世', '逝世', '病逝', '离开了人世', '离开人世', '离世', '辞世'}
        set_exp = {'之后', '后'}
        for sentence in sentences:
            if self.int_birth != 0:
                break
            if sentence != "":
                sentence, list_symbol = utils.short_data(sentence)
                for str_birth in set_birth:
                    if str_birth in sentence:
                        mat_year4 = re.findall(r"(\d{4}年)", sentence)
                        if len(mat_year4) != 0:
                            self.int_birth = int((mat_year4[0].strip("年")).encode("utf-8"))
                            break
                for str_death in set_death:
                    index = sentence.find(str_death)
                    if index > 0 and sentence[index + len(str_death):index + len(str_death)] not in set_exp:
                        mat_year4 = re.findall(r"(\d{4}年)", sentence)
                        mat_old = re.findall(r"(\d{2,3}岁)", sentence)
                        if len(mat_year4) != 0 and len(mat_old) != 0:
                            int_death = int((mat_year4[-1].strip("年")).encode("utf-8"))
                            int_old = int((mat_old[-1].strip("岁")).encode("utf-8"))
                            self.int_birth = int_death - int_old
                            break

    def ner(self, ori_sentence):
        print("\nner...")
        # 简化书名号/引号/括号内内容
        sentence, list_symbol = utils.short_data(ori_sentence)
        tuple_ners = self.nlp.ner(sentence)
        # 转换原格式
        ners = []
        for tuple_ner in tuple_ners:
            ners.append(list(tuple_ner))
        # 正则优化Ners
        list_date, list_date_pos = self.__get_date(ners)
        list_per, list_per_pos = self.__get_per(ners)
        list_loc, list_loc_pos = self.__get_loc(ners)
        # print('')
        # print('sent:', sentence)
        # print('ners:', ners)
        # print('date:', list_date)
        # print('per:', list_per)
        # print('loc:', list_loc)
        # 计算分割点
        list_split_pos = self.__get_split_pos(ners, list_date_pos)
        # 还原书名号/引号/括号内内容
        ners = utils.long_ners(ners, list_symbol)
        # 划分子句实体
        list_ners = []
        for i in range(len(list_split_pos)):
            sub_list_date, sub_list_per, sub_list_loc, sub_list_sentence = [], [], [], [""]
            for j in range(len(list_date)):
                if list_split_pos[i][0] < list_date_pos[j] < list_split_pos[i][1]:
                    sub_list_date.append(list_date[j])
            for j in range(len(list_per)):
                if list_split_pos[i][0] < list_per_pos[j] < list_split_pos[i][1]:
                    sub_list_per.append(list_per[j])
            for j in range(len(list_loc)):
                if list_split_pos[i][0] < list_loc_pos[j] < list_split_pos[i][1]:
                    sub_list_loc.append(list_loc[j])
            for j in range(len(ners)):
                if list_split_pos[i][0] < j < list_split_pos[i][1]:
                    sub_list_sentence[0] += ners[j][0]
            if int(i) != len(list_split_pos) - 1:
                sub_list_sentence[0] += "。"
            # 分句内单一化时间
            if len(sub_list_date) > 1:
                list_year = re.findall(r"(\d{4})", sub_list_date[i])
                list_year = [int(item_year) for item_year in list_year]
                min_year, max_year = min(list_year), max(list_year)
                if min_year == max_year:
                    sub_list_date = [str(min_year) + '年']
                else:
                    sub_list_date = [str(min_year) + '-' + str(max_year) + '年']
            # 去掉过短时间分句
            if len(sub_list_date) > 0 and len(sub_list_sentence[0]) < 10:
                if sub_list_sentence[0].find(sub_list_date[0]) > 1:
                    sub_list_date = []
            # print(sub_list_sentence)
            # print(sub_list_date)
            # print(sub_list_per)
            # print(sub_list_loc)
            list_ners.append([sub_list_date, sorted(set(sub_list_per), key=sub_list_per.index), sorted(set(sub_list_loc), key=sub_list_loc.index), sub_list_sentence])
        return list_ners

    def __get_date(self, ners):
        # 提取时间实体
        list_date = []
        list_date_pos = []
        int_age = 0
        set_zh = {'一', '二', '三', '四', '五', '六', '七', '八', '九', '十'}
        set_num = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}.union(set_zh)
        set_date = {'一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '年', '月', '日', '-', '月份', '号'}
        for i in range(len(ners)):
            if ners[i][1] == 'DATE' and len(set(ners[i][0]).difference(set(ners[i][0]).intersection(set_date))) != 0:
                ners[i][1] = 'TMP_DATE'
            if i > 0 and ners[i][1] == 'DATE' and ners[i - 1][1] == 'DATE':
                pop_word = list_date.pop()
                list_date.append(pop_word + ners[i][0])
            elif 0 < i < len(ners) - 1 and ners[i][0] == '的' and ners[i - 1][1] == 'DATE' and ners[i + 1][1] == 'DATE':
                pop_word = list_date.pop()
                list_date.append(pop_word + ners[i][0])
            # 识别岁数
            elif self.int_birth != 0 and (ners[i][0] == '岁' or ners[i][0] == '岁时') and ners[i - 1][1] == 'NUMBER' and len(set(ners[i - 1][0]).difference(set(ners[i - 1][0]).intersection(set_num))) == 0:
                list_date.append(ners[i - 1][0] + '岁')
                int_age += 1
                list_date_pos.append(int(i))
            elif i > 0 and (ners[i][0] == '至' or ners[i][0] == '到' or ners[i][0] == '-' or ners[i][0] == '—' or ners[i][0] == '－' or ners[i][0] == '~') and ners[i - 1][1] == 'DATE' and ners[i + 1][1] == 'DATE':
                ners[i][1] = 'DATE'
                pop_word = list_date.pop()
                list_date.append(pop_word + '-')
            elif ners[i][1] == 'DATE':
                list_date.append(ners[i][0])
                list_date_pos.append(int(i))
        # 转换中文时间为阿拉伯时间
        for i in range(len(list_date)):
            if bool(set_zh.intersection(set(list_date[i]))):
                list_date[i] = utils.zh2number(list_date[i])
        # 补年龄(年)
        if self.int_birth != 0 and len(list_date) == int_age:
            for i in range(len(list_date)):
                if "岁" in list_date[i]:
                    list_date[i] = str(self.int_birth + int((list_date[i].strip("岁")).encode("utf-8"))) + "年"
        # 补全年(月日)
        for i in range(len(list_date)):
            index = list_date[i].find('-')
            if index >= 0:
                if list_date[i][index - 1] in set_num:
                    list_date[i] = list_date[i][:index] + list_date[i][-1] + list_date[i][index:]
        for i in range(len(list_date)):
            list_date[i] = list_date[i].replace("的", "")
            list_date[i] = list_date[i].replace("月份", "月")
            if "年" in list_date[i]:
                mat_year2 = re.findall(r"(\d{2}年)", list_date[i])
                mat_year3 = re.findall(r"(\d{3}年)", list_date[i])
                mat_year4 = re.findall(r"(\d{4}年)", list_date[i])
                set_year2 = set(mat_year2).difference(set(mat_year4)).difference(set(mat_year3))
                if len(mat_year4) != 0:
                    self.last_year = mat_year4[-1]
                elif len(set_year2) != 0:
                    for item in set_year2:
                        list_date[i] = list_date[i].replace(item, self.last_year[0] + self.last_year[1] + item)
            elif "月" in list_date[i] and self.last_year != "":
                list_date[i] = self.last_year + list_date[i]
        # 剔除不满足时间实体
        list_date_format = []
        list_date_format_pos = []
        for i in range(len(list_date)):
            if "年" in list_date[i] and ners[list_date_pos[i - 1]][0] != "把":
                list_date_format.append(list_date[i])
                list_date_format_pos.append(list_date_pos[i])
        return list_date_format, list_date_format_pos

    @staticmethod
    def __get_per(ners):
        # 韋瓦第|伯恩斯坦|卢托斯瓦夫斯基|吕利|圣-桑|埃尔加|库普兰|瓦格纳
        list_per = []
        list_per_pos = []
        set_not = {'们'}
        set_name = {'.', '·', ' '}
        for i in range(len(ners)):
            if i + 2 < len(ners) and ners[i + 1][0] in set_name:
                if ners[i][1] == 'PERSON' \
                        or (ners[i][0].encode('UTF-8').isalpha() and len(ners[i][0]) == 1) \
                        or ners[i + 2][1] == 'PERSON' \
                        or (ners[i + 2][0].encode('UTF-8').isalpha() and len(ners[i + 2][0]) == 1) \
                        :
                    ners[i][1] = 'PERSON'
                    ners[i + 1][1] = 'PERSON'
                    ners[i + 2][1] = 'PERSON'
            elif i + 2 < len(ners) and ners[i + 1][0][0] in set_name:
                if ners[i][1] == 'PERSON' \
                        or (ners[i][0].encode('UTF-8').isalpha() and len(ners[i][0]) == 1) \
                        or ners[i + 1][1] == 'PERSON':
                    ners[i][1] = 'PERSON'
                    ners[i + 1][1] = 'PERSON'
            elif i + 1 < len(ners) and ners[i][0][-1] in set_name:
                if ners[i][1] == 'PERSON' \
                        or ners[i + 1][1] == 'PERSON' \
                        or (ners[i + 1][0].encode('UTF-8').isalpha() and len(ners[i + 1][0]) == 1) \
                        :
                    ners[i][1] = 'PERSON'
                    ners[i + 1][1] = 'PERSON'
            if ners[i][1] == 'PERSON' and ners[i - 1][1] == 'PERSON':
                pop_word = list_per.pop()
                list_per.append(pop_word + ners[i][0])
            elif ners[i][1] == 'PERSON':
                list_per.append(ners[i][0])
                list_per_pos.append(int(i))
        # 剔除不满足实体
        list_per_format = []
        list_per_format_pos = []
        for i in range(len(list_per)):
            if ners[list_per_pos[i] - 1][0] != "在" \
                    and len(set(list_per[i]).intersection(set_not)) == 0 \
                    and list_per[i][-1] != "于" \
                    and ners[list_per_pos[i] - 1][1] != "CITY" \
                    and ners[list_per_pos[i] - 1][1] != "COUNTRY" \
                    and list_per[i][0] not in set_name \
                    and list_per[i][-1] not in set_name:
                list_per_format.append(list_per[i])
                list_per_format_pos.append(list_per_pos[i])
        return list_per_format, list_per_format_pos

    @staticmethod
    def __get_loc(ners):
        list_loc = []
        list_loc_pos = []
        for i in range(len(ners)):
            if ners[i][1] == 'CITY' or ners[i][1] == 'COUNTRY' and len(ners[i][0]) > 1:
                list_loc.append(ners[i][0])
                list_loc_pos.append(int(i))
        return list_loc, list_loc_pos

    @staticmethod
    def __get_split_pos(ners, list_date_pos):
        list_list_date_pos, sub_list_date_pos, list_comma_pos = [], [], []
        last_comma_pos = -1
        for i in range(len(ners)):
            if ners[i][0] == '，' or int(i) == len(ners) - 1:
                list_comma_pos.append(int(i))
                for date_pos in list_date_pos:
                    if last_comma_pos < date_pos < i:
                        sub_list_date_pos.append(date_pos)
                if len(sub_list_date_pos) != 0:
                    list_list_date_pos.append(sub_list_date_pos)
                    sub_list_date_pos = []
                    last_comma_pos = int(i)
        list_split_pos = []
        if len(list_list_date_pos) <= 1:
            list_split_pos.append((-1, float('inf')))
        else:
            i = 1
            last_split_pos = -1
            while i < len(list_list_date_pos):
                for j in range(len(list_comma_pos)):
                    if list_comma_pos[j] < list_list_date_pos[i][0] < list_comma_pos[j + 1]:
                        list_split_pos.append((last_split_pos, list_comma_pos[j]))
                        last_split_pos = list_comma_pos[j]
                        break
                i += 1
            list_split_pos.append((list_split_pos[-1][1], float('inf')))
        return list_split_pos


if __name__ == "__main__":
    model = NLP()
    model.ner("1901年，1745年-1348年,15年-18年,9月")
