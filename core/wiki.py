import os
import sys
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import re
from core.utils import *

root_path = os.path.abspath('..')


class WikiCrawler:
    def __init__(self):
        self.path_wiki = root_path + "\\data\\wiki"
        self.path_clean1 = root_path + "\\data\\clean_1"
        if not os.path.exists(self.path_wiki):
            os.mkdir(self.path_wiki)

    def get_name(self):
        out_path = self.path_wiki
        file_path = out_path + '/list.csv'
        f = open(file_path, "w", encoding="utf-8")
        f.write("姓名,\n")

        # 爬取时间段[古典音乐家]---------------------------
        html = urlopen(
            "https://zh.wikipedia.org/wiki/%E5%8F%A4%E5%85%B8%E9%9F%B3%E6%A8%82%E4%BD%9C%E6%9B%B2%E5%AE%B6%E5%88%97"
            "%E8%A1%A8 "
        ).read().decode('utf-8')  # if has Chinese, apply decode()
        # 获取子链接[某时间段]
        soup = BeautifulSoup(html, features="html.parser")
        for node_div in soup.find_all("div", {"class": "hatnote navigation-not-searchable"}):
            period = node_div.find_previous("h2").find("span", {"class": "mw-headline"}).text
            print('\n')
            print('正在爬取' + period + '的音乐家 ...')
            # 爬取音乐家列表[某时间段]---------------------------
            html = urlopen(
                "https://zh.wikipedia.org" + node_div.a['href']
            ).read().decode('utf-8')  # if has Chinese, apply decode()
            # 获取子链接[某音乐家]
            soup = BeautifulSoup(html, features="html.parser")
            for node_time in soup.find_all("span", {"class": "mw-headline"}):
                node_h2 = node_time.parent
                node_ul = node_h2.next_sibling
                while node_ul == '\n':
                    node_ul = node_ul.next_sibling
                if node_ul.name == 'ul':
                    nodes_a = node_ul.find_all("a")  # 只获取粗体
                    for node_a in nodes_a:
                        if node_a != -1 and node_a is not None:
                            if node_a.has_attr("class"):
                                if node_a['class'] in [['new'], ['extiw']]:
                                    continue
                            html_sub = urlopen(
                                "https://zh.wikipedia.org" + node_a['href']
                            ).read().decode('utf-8')  # if has Chinese, apply decode()
                            # 获取标题节点
                            soup_sub = BeautifulSoup(html_sub, features="html.parser")
                            node_h1 = soup_sub.find("h1", {"class": "firstHeading"})
                            [s.extract() for s in node_h1.find_all({"class": "mw-editsection"})]
                            title = th2zh(del_bracket(sbc2dbc(node_h1.text)))
                            title = title.replace(" ", "")
                            title = title.replace("-", "·")
                            title = title.replace("-", "·")
                            print(title + ' ... ')
                            print("https://zh.wikipedia.org" + node_a['href'])
                            f.write(title + ",\n")
        f.close()

    def get_wiki(self, mincount=100):
        out_path = self.path_wiki
        df = pd.read_csv(out_path + '/list.csv', encoding="utf-8")
        all_names = df[['姓名']].values

        # 爬取时间段[古典音乐家]---------------------------
        html = urlopen(
            "https://zh.wikipedia.org/wiki/%E5%8F%A4%E5%85%B8%E9%9F%B3%E6%A8%82%E4%BD%9C%E6%9B%B2%E5%AE%B6%E5%88%97"
            "%E8%A1%A8 "
        ).read().decode('utf-8')  # if has Chinese, apply decode()
        # 获取子链接[某时间段]
        soup = BeautifulSoup(html, features="html.parser")
        i = 0
        for node_div in soup.find_all("div", {"class": "hatnote navigation-not-searchable"}):
            if i < 0:
                i +=1
                continue
            period = node_div.find_previous("h2").find("span", {"class": "mw-headline"}).text
            print('\n')
            print('正在爬取' + period + '的音乐家 ...')
            # 爬取音乐家列表[某时间段]---------------------------
            html = urlopen(
                "https://zh.wikipedia.org" + node_div.a['href']
            ).read().decode('utf-8')  # if has Chinese, apply decode()
            # 获取子链接[某音乐家]
            soup = BeautifulSoup(html, features="html.parser")
            for node_time in soup.find_all("span", {"class": "mw-headline"}):
                node_h2 = node_time.parent
                node_ul = node_h2.next_sibling
                while node_ul == '\n':
                    node_ul = node_ul.next_sibling
                if node_ul.name == 'ul':
                    nodes_a = node_ul.find_all("a")
                    for node_a in nodes_a:
                        if node_a == -1 or node_a is None:
                            continue
                        else:
                            html_sub = urlopen(
                                "https://zh.wikipedia.org" + node_a['href']
                            ).read().decode('utf-8')  # if has Chinese, apply decode()
                            soup_sub = BeautifulSoup(html_sub, features="html.parser")
                            list_html = []
                            node_h1 = soup_sub.find("h1", {"class": "firstHeading"})
                            node_card = soup_sub.find("table", {"class": "infobox biography vcard"})
                            node_life = soup_sub.find("span", {"id": "生平"})
                            node_music = soup_sub.find("span", {"id": "音樂生涯"})
                            # 获取全名
                            [s.extract() for s in node_h1.find_all({"class": "mw-editsection"})]
                            title = th2zh(del_bracket(sbc2dbc(node_h1.text)))
                            title = title.replace("-", "·")
                            title = title.replace("-", "·")
                            title = title.replace(" ", "")
                            file_path = out_path + '/' + title + ".txt"
                            if os.path.exists(file_path):
                                continue
                            print("https://zh.wikipedia.org" + node_a['href'])
                            if node_card == -1 or node_card is None or node_life == -1 or node_life is None:
                                print(title, ": no card/life")
                                continue
                            else:
                                # 获取卡片html
                                for node_card_th in node_card.find_all('th'):
                                    if node_card_th.text == '出生' or node_card_th.text == '逝世':
                                        info = th2zh(del_blank(del_bracket(sbc2dbc(node_card_th.parent.text))))
                                        infos = []
                                        if '年' not in info:
                                            continue
                                        if '日' in info:
                                            infos = re.split('(\n|日)', info)
                                        elif '月' in info:
                                            infos = re.split('(\n|月)', info)
                                        elif '年' in info:
                                            infos = re.split('(\n|年)', info)
                                        if len(infos) == 5:
                                            list_html.append(
                                                "<p>%s，他在%s%s。</p>" % (infos[2] + infos[3], infos[4], infos[0]))
                                if len(list_html) == 0:
                                    print(title, ": no birth/death")
                                    continue
                                # 获取生平html
                                node_next = node_life.parent.next_sibling
                                while node_next != -1 and node_next is not None and node_next.name != 'h2':
                                    if node_next.name == 'p':
                                        [s.extract() for s in node_next.find_all('sup')]
                                        # 替换全名
                                        for node_next_a in node_next.find_all('a'):
                                            if node_next_a.has_attr("class"):
                                                if node_next_a['class'] in [['new'], ['extiw']]:
                                                    continue
                                            html = urlopen(
                                                "https://zh.wikipedia.org" + node_next_a['href']
                                            ).read().decode('utf-8')  # if has Chinese, apply decode()
                                            soup_a = BeautifulSoup(html, features="html.parser")
                                            node_a_h1 = soup_a.find("h1", {"class": "firstHeading"})
                                            [s.extract() for s in node_a_h1.find_all({"class": "mw-editsection"})]
                                            title = th2zh(del_bracket(sbc2dbc(node_a_h1.text)))
                                            title = title.replace("-", "·")
                                            title = title.replace("-", "·")
                                            if title in all_names:
                                                node_next_a.string = "{" + title + "}"
                                            else:
                                                node_next_a.string = title
                                        list_html.append(str(node_next))
                                    node_next = node_next.next_sibling

                            # 获取txt
                            text_life = ''
                            for html_life in list_html:
                                soup_life = BeautifulSoup(html_life, features="html.parser")
                                for string in soup_life.stripped_strings:
                                    text_life += string
                                text_life += "\n"
                            if len(text_life) >= mincount:
                                text_life = th2zh(text_life)
                                print(node_h1.text + '... ' + str(len(text_life)) + " char")
                                f = open(file_path, "w", encoding="utf-8")
                                f.write(text_life)
                                f.close()
                                print(text_life)


if __name__ == "__main__":
    wikiCrawler = WikiCrawler()
    # wikiCrawler.get_name()
    wikiCrawler.get_wiki()
