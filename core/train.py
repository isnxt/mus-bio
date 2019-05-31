# -*- coding: utf-8
import os

from core import utils


class WordTagger:
    def __init__(self):
        self.root_path = os.path.abspath('..')
        self.path_cache = self.root_path + "\\data\\train\\regexner\\cache"
        self.path_in = self.root_path + "\\data\\train\\regexner\\base"
        self.path_out = self.root_path + "\\data\\train\\regexner\\out"

        if not os.path.exists(self.path_cache):
            os.mkdir(self.path_cache)

    def tag_person(self, file_in="wiki-person.txt", file_out="wiki-name-tag.tab"):
        fr = open(self.path_in + "\\" + file_in, 'r', encoding="utf-8")
        data_in = fr.read()
        data_lines = (data_in + "\n" + utils.th2zh(data_in)).split('\n')
        list_names = []
        set_del = {"", " ", "\n"}
        for line in data_lines:
            if line not in set_del:
                list_names.append(line)
                if "·" in line:
                    if "-" not in line and " " not in line:
                        first_name = line.split("·")[-1]
                        if len(first_name) != 1:
                            list_names.append(first_name)
                    list_names.append(line.replace("·", "-"))
                    list_names.append(line.replace("·", " "))
                elif "-" in line:
                    if " " not in line and "·" not in line:
                        first_name = line.split("-")[-1]
                        if len(first_name) != 1:
                            list_names.append(first_name)
                    list_names.append(line.replace("-", "·"))
                    list_names.append(line.replace("-", " "))
        fw = open(self.path_cache + "\\" + file_out, 'w', encoding="utf-8")
        for item in sorted(set(list_names)):
            fw.write(item + "\tPERSON\n")
        fr.close()
        fw.close()

    def join_tag(self):
        files_in = os.listdir(self.path_cache)
        data_tab = ""
        for file_in in files_in:
            if os.path.splitext(file_in)[-1] == ".tab":
                fr = open(self.path_cache + "\\" + file_in, 'r', encoding="utf-8")
                data_tab += fr.read()
                fr.close()
        fw = open(self.path_out + "\\jg-regexner.txt", 'w', encoding="utf-8")
        fw.write(data_tab)
        fw.close()

    def tag_word(self):
        files_in = os.listdir(self.path_in)
        for file_in in files_in:
            if os.path.splitext(file_in)[-1] == ".txt":
                file_name = os.path.splitext(file_in)[0]
                file_type = file_name.split("-")[-1]
                if file_type == "person":
                    self.tag_person(file_in=file_name + ".txt", file_out=file_name + ".tab", )


if __name__ == "__main__":
    wordTagger = WordTagger()
    wordTagger.tag_word()
    wordTagger.join_tag()
