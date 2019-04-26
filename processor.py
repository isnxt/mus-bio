import re
import zhconv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os


def clean_data(path_in="./data/wiki", path_out='./data/cleaned'):
    if not os.path.exists(path_out):
        os.mkdir(path_out)
    files = os.listdir(path_in)
    for file in files:
        fr = open(path_in + "/" + file, "r", encoding="utf-8")
        str = fr.read()
        # 标准化字符
        str = str.replace('(', '（')
        str = str.replace(')', '）')
        str = str.replace(',', '，')
        # 去注释
        str = re.sub('\[.*?\]', '', str)
        str1 = ''
        # 去括号
        paren = 0
        for c in str:
            if c == '（':
                paren += 1
            elif c == '）':
                paren -= 1
            elif paren == 0:
                str1 += c
        # 去空格
        char_alpha = ['']
        str2 = ''
        for i in range(len(str1)):
            if str1[i] == ' ' and str1[i - 1].isalpha() and str1[i + 1].isalpha():
                str2 += '·'
                continue
            elif str1[i] == ' ':
                continue
            str2 += str1[i]

        # 换行
        # str2 = str2.replace('。', '。\n')
        # 将繁体转换成简体
        str2 = zhconv.convert(str2, 'zh-cn')

        fw = open(path_out + '/' + file, "w", encoding="utf-8")
        fw.write(str2)
        fw.close()


def crawl_data(path_out="./data/wiki"):
    if not os.path.exists(path_out):
        os.mkdir(path_out)
    # 爬取时间段[古典音乐家]---------------------------
    html = urlopen("https://zh.wikipedia.org/wiki/%E5%8F%A4%E5%85%B8%E9%9F%B3%E6%A8%82%E4%BD%9C%E6%9B%B2%E5%AE%B6%E5%88%97%E8%A1%A8"
                   ).read().decode('utf-8')  # if has Chinese, apply decode()
    # 获取子链接[某时间段]
    soup = BeautifulSoup(html, features="html.parser")
    for node_div in soup.find_all("div", {"class": "hatnote navigation-not-searchable"}):
        period = node_div.find_previous("h2").find("span", {"class": "mw-headline"}).text
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
                nodes_bold = node_ul.find_all("b")  # 只获取粗体
                for node_bold in nodes_bold:
                    if node_bold != -1 and node_bold is not None and node_bold.a is not None:
                        print(node_bold.text + ' ...')
                        html_sub = urlopen(
                            "https://zh.wikipedia.org" + node_bold.a['href']
                        ).read().decode('utf-8')  # if has Chinese, apply decode()
                        # 获取生平标题节点
                        soup_sub = BeautifulSoup(html_sub, features="html.parser")
                        node_life = soup_sub.find("span", {"id": "生平"})
                        if node_life != -1 and node_life is not None:
                            node_next = node_life.parent.next_sibling
                            # 获取生平内容html
                            html_life = ""
                            while node_next != -1 and node_next is not None and node_next.name != 'h2':
                                if node_next.name == 'p':
                                    html_life += str(node_next)
                                node_next = node_next.next_sibling
                            # 获取生平内容txt
                            soup_life = BeautifulSoup(html_life, features="html.parser")
                            text_life = ''
                            for string in soup_life.stripped_strings:
                                text_life += string
                            f = open(path_out + '/' + node_bold.text + ".txt", "w", encoding="utf-8")
                            f.write(text_life)
                            f.close()




if __name__ == "__main__":
    # crawl_data()
    clean_data()
