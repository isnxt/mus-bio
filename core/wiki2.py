import os
import sys
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import re
import jieba.analyse
from core.utils import *
from stanfordcorenlp import StanfordCoreNLP

root_path = os.path.abspath('..')
# %% 配置
# 输出设置

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


class WikiCleaner:
    def __init__(self):
        self.path_wiki = root_path + "\\data\\wiki"
        self.path_clean1 = root_path + "\\data\\clean_1"
        self.path_clean2 = root_path + "\\data\\clean_2"
        self.path_clean3 = root_path + "\\data\\clean_3"
        self.path_clean4 = root_path + "\\data\\clean_4"
        self.path_clean5 = root_path + "\\data\\clean_5"

        if not os.path.exists(self.path_wiki):
            os.mkdir(self.path_wiki)

    def clean_1(self):
        files = os.listdir(self.path_wiki)
        for file in files:
            if os.path.splitext(file)[-1] == ".txt":
                in_path = self.path_wiki + "\\" + file
                out_path = self.path_clean1 + "\\" + file
                done_path = self.path_clean1 + "\\done\\" + file
                if os.path.exists(out_path) or os.path.exists(done_path):
                    continue
                fr = open(in_path, encoding='utf-8')
                lines = fr.readlines()
                cleaned = ""

                # 出生日期
                birth = ""
                death = ""
                set_birth = {"出生", "诞生", '生于'}
                set_death = {"逝世"}

                for i in range(len(lines)):
                    if any(verb in lines[i] for verb in set_birth):
                        birthyear = re.findall('(\d{4}年)', lines[i])
                        if len(birthyear) == 1:
                            birth = birthyear[0]
                            break
                    if any(verb in lines[i] for verb in set_death):
                        deathyear = re.findall('(\d{4}年)', lines[i])
                        if len(deathyear) == 1:
                            death = deathyear[0]
                            break
                if birth == "" and death == "":
                    print(file + " no birth/death")
                    continue

                for i in range(len(lines)):
                    line = lines[i]
                    # 繁体转简体;删除括号;中英字符
                    line = th2zh(del_bracket(sbc2dbc(line)))
                    line = line.rstrip()
                    # 分句
                    left, right, end = ['“', "《"], ['”', "》"], ['？', '！', '。']
                    stats = 0
                    para = ""
                    for i in range(len(line)):
                        if line[i] in left:
                            stats += 1
                        elif line[i] in right:
                            stats -= 1
                        if stats == 0 and line[i] in end:
                            para += line[i] + '\n'
                        elif stats == 0 and line[i] == '”' and line[i - 1] in end:
                            para += line[i] + '\n'
                        else:
                            para += line[i]
                    sents = para.split('\n')
                    # 日期筛选
                    time = {"年", "月", "日", "岁",
                            "一", "二", "两", "三", "四", "五", "六", "七", "八", "九", "零", "十",
                            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
                    for i in range(len(sents)):
                        if any(verb in sents[i] for verb in time):
                            cleaned += sents[i] + '\n'

                fr.close()

                if len(cleaned) > 5:
                    fw = open(out_path, "w", encoding="utf-8")
                    fw.write(cleaned)
                    fw.close()

    def clean_2(self):
        files = os.listdir(self.path_clean1 + "\\done\\")
        for file in files:
            if os.path.splitext(file)[-1] == ".txt":
                in_path = self.path_clean1 + "\\done\\" + file
                out_path = self.path_clean2 + "\\" + file
                done_path = self.path_clean2 + "\\done\\" + file
                if os.path.exists(out_path) or os.path.exists(done_path):
                    continue
                # 出生日期
                fr = open(in_path, encoding='utf-8')
                lines = fr.readlines()
                cleaned = ""
                # 出生日期
                birth = ""
                death = ""
                set_birth = {"出生", "诞生", '生于'}
                set_death = {"逝世"}

                for i in range(len(lines)):
                    if any(verb in lines[i] for verb in set_birth):
                        birthyear = re.findall('(\d{4}年)', lines[i])
                        if len(birthyear) == 1:
                            birth = birthyear[0]
                            break
                    if any(verb in lines[i] for verb in set_death):
                        deathyear = re.findall('(\d{4}年)', lines[i])
                        if len(deathyear) == 1:
                            death = deathyear[0]
                            break
                if birth == "" and death == "":
                    print(file + " no birth/death")
                    continue
                # 替换岁数
                for i in range(len(lines)):
                    line = lines[i].rstrip()
                    zh = re.findall('([一二两三四五六七八九零十百\d]+[岁日月年世纪]+)', line)
                    for i in range(len(zh)):
                        line = line.replace(zh[i], zh2number(zh[i]))
                        if '岁' in line:
                            line = age2year(birth, death, line)
                    cleaned += line + '\n'
                fr.close()

                fw = open(out_path, "w", encoding="utf-8")
                fw.write(cleaned)
                fw.close()

    def clean_3(self):
        files = os.listdir(self.path_clean1 + "\\done\\")
        for file in files:
            if os.path.splitext(file)[-1] == ".txt":
                in_path = self.path_clean2 + "\\done\\" + file
                out_path = self.path_clean3 + "\\" + file
                done_path = self.path_clean3 + "\\done\\" + file
                if os.path.exists(out_path) or os.path.exists(done_path):
                    continue
                fr = open(in_path, encoding='utf-8')
                lines = fr.readlines()
                allname = file[:-4]
                firstname = allname.split('·')[-1]
                cleaned = ""

                for i in range(len(lines)):
                    line = lines[i].rstrip()
                    if line == "":
                        continue
                    # 标准化时间
                    line = del_blank(line)
                    line = sbc2dbc(line)
                    match = re.findall('(\d{4}年)', line)
                    for i in range(len(match)):
                        year = match[i]
                        line = line.replace(year, year[:4])
                    match = re.findall('(\d{4})', line)
                    for i in range(len(match)):
                        year = match[i]
                        line = line.replace(year, year + '年')
                    match = re.findall('(\d{4}年至\d{4})', line)
                    for i in range(len(match)):
                        year = match[i]
                        line = line.replace(year, year.replace('至', '-'))
                    match = re.findall('(\d{4}年到\d{4})', line)
                    for i in range(len(match)):
                        year = match[i]
                        line = line.replace(year, year.replace('到', '-'))
                    # 替换代词
                    line1 = ""
                    for i in range(len(line)):
                        if line[i] == '他' or line[i] == '她' and i < len(line) - 1 and line[i + 1] != "们":
                            if i > 0 and line[i - 1] == "吉":
                                line1 += line[i]
                            else:
                                line1 += allname + line[i + 1:]
                                break
                        else:
                            line1 += line[i]
                    line = line1
                    # 填补名字
                    line2, start = "", 0
                    while True:
                        index = line.find(firstname, start)
                        if index == -1:
                            line2 += line[start:]
                            break
                        elif index == 0:
                            line2 += line[start:index] + allname
                            start = index + len(firstname)
                        elif index > 0 and line[index - 1] != '·':
                            line2 += line[start:index] + allname
                            start = index + len(firstname)
                        else:
                            line2 += line[start:index] + firstname
                            start = index + len(firstname)
                    line = line2
                    # 添加名字
                    if line.find(allname) == -1:
                        if line.find('日，') != -1:
                            index = line.find('日，') + 2
                            line = line[:index] + allname + line[index:]
                        elif line.find('月，') != -1:
                            index = line.find('月，') + 2
                            line = line[:index] + allname + line[index:]
                        elif line.find('年，') != -1:
                            index = line.find('年，') + 2
                            line = line[:index] + allname + line[index:]
                        elif line.rfind('日') != -1:
                            index = line.rfind('日') + 1
                            line = line[:index] + '，' + allname + line[index:]
                        elif line.rfind('月') != -1:
                            index = line.rfind('月') + 1
                            line = line[:index] + '，' + allname + line[index:]
                        elif line.rfind('年') != -1:
                            index = line.rfind('年') + 1
                            line = line[:index] + '，' + allname + line[index:]
                        else:
                            print('cannot add name (%s): %s' % (file, line))
                            break
                    # 引用名字
                    line = line.replace(allname, '{' + allname + '}')
                    # 引用时间
                    match = re.finditer('(\d{4}年\d+月\d+日-\d{4}年\d+月\d+日)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or line[i.start() - 1] != '[':
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    match = re.finditer('(\d{4}年\d+月-\d{4}年\d+月)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or line[i.start() - 1] != '[':
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    match = re.finditer('(\d{4}年-\d{4}年)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or line[i.start() - 1] != '[':
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    match = re.finditer('(\d{4}年\d+月\d+日)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or (line[i.start() - 1] != '[' and line[i.end()] != ']'):
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    match = re.finditer('(\d{4}年\d+月)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or (line[i.start() - 1] != '[' and line[i.end()] != ']'):
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    match = re.finditer('(\d{4}年)', line)
                    rep = []
                    for i in match:
                        if i.start() == 0 or (line[i.start() - 1] != '[' and line[i.end()] != ']'):
                            rep.append(line[i.start():i.end()])
                    for i in range(len(rep)):
                        line = line.replace(rep[i], '[' + rep[i] + ']')
                    print(line)
                    cleaned += line + '\n'

                fr.close()

                fw = open(out_path, "w", encoding="utf-8")
                fw.write(cleaned)
                fw.close()

    def clean_4(self):
        files = os.listdir(self.path_clean3 + "\\done\\")
        locs = []
        nlp = StanfordCoreNLP('D:\\Project\\NLP-zh\\corenlp', port=9000, lang='zh')
        for file in files:
            if os.path.splitext(file)[-1] != ".txt":
                continue

            in_path = self.path_clean3 + "\\done\\" + file
            out_path = self.path_clean4 + "\\" + file
            done_path = self.path_clean4 + "\\done\\" + file
            if os.path.exists(out_path) or os.path.exists(done_path):
                continue
            fr = open(in_path, encoding='utf-8')
            allname = file[:-4]
            lines = fr.readlines()
            cleaned = ""
            for i in range(len(lines)):
                line = lines[i].rstrip()
                if line == "":
                    continue
                if int(i) in [0, 1]:
                    pattern = '(，{' + allname + '}在.+(出生|逝世)。)'
                    match = re.finditer(pattern, line)
                    for i in match:
                        ns = line[i.start() + len('，{' + allname + '}在'):i.end() - 3]
                        line = line.replace(ns, '<' + ns + '>')
                        locs.append(ns)
                        break
                    cleaned += line + '\n'
                    continue
                tuple_ners = nlp.ner(line)
                ners = []
                for tuple_ner in tuple_ners:
                    ners.append(list(tuple_ner))
                list_loc = []
                for i in range(len(ners)):
                    if ners[i][1] == 'CITY' or ners[i][1] == 'COUNTRY' or ners[i][1] == 'LOCATION' and len(
                            ners[i][0]) > 1:
                        list_loc.append(ners[i][0])
                for loc in list_loc:
                    line = line.replace(loc, '<' + loc + '>')
                    locs.append(loc)
                    break
                cleaned += line + '\n'
            fr.close()
            if len(lines) == 2:
                fw = open(done_path, "w", encoding="utf-8")
            else:
                fw = open(out_path, "w", encoding="utf-8")
            fw.write(cleaned)
            fw.close()
        print(locs)
        nlp.close()

    def clean_5(self):
        files = os.listdir(self.path_clean4 + "\\done\\")
        results = pd.DataFrame(columns=('time', 'person', 'location', 'thing'))
        for file in files:
            if os.path.splitext(file)[-1] != ".txt":
                continue
            in_path = self.path_clean4 + "\\done\\" + file
            out_path = self.path_clean5 + "\\" + file
            done_path = self.path_clean5 + "\\done\\" + file
            # if os.path.exists(out_path) or os.path.exists(done_path):
            #     continue
            fr = open(in_path, encoding='utf-8')
            lines = fr.readlines()
            last_loc = ""
            result = pd.DataFrame(columns=('time', 'person', 'location', 'thing'))
            for i in range(len(lines)):
                line = lines[i].rstrip()
                if line == "":
                    continue
                if line[-1]!='。' and line[-1]!='，':
                    print(line)
                list_time = [i for i in re.findall('\[(.*?)\]', line)]
                list_loc = [i for i in re.findall('<(.*?)>', line)]
                list_per = [i for i in re.findall('\{(.*?)\}', line)]
                list_time = drop_dup(list_time)
                list_loc = drop_dup(list_loc)
                list_per = drop_dup(list_per)
                for time in list_time:
                    for per in list_per:
                        for loc in list_loc:
                            df = pd.DataFrame({'time': [time], 'person': [per], 'location': [loc], 'thing': [line]})
                            result = result.append(df, ignore_index=True)
            result = result.sort_values(by=['time'])
            result = result.fillna(method='ffill')
            result = result.fillna(method='bfill')
            fr.close()
            result.to_csv(out_path, index=False)
            results = pd.concat([result, results], ignore_index=True)
        print(results)
        results.to_csv('../out/test.csv', index=False,sep='|')
        for col in range(results.shape[0]):
            results.thing[col] = sbc2dbc(re.sub('(\[|\]|<|>|\{|\})', '', (results.thing[col])))
        print(results.describe())
        results.to_csv('../out/all.csv', index=False,sep='|')


if __name__ == "__main__":
    wikiCrawler = WikiCleaner()
    wikiCrawler.clean_1()
    # wikiCrawler.clean_2()
    # wikiCrawler.clean_3()
    wikiCrawler.clean_5()
