import os
import sys
import chardet
from core import nlp
root_path = os.path.abspath('.')

def read_data(file_path):
    print(file_path)
    fb = open(file_path, 'rb')
    detected = chardet.detect(fb.readline())
    print(detected)
    if detected.get('encoding') == 'utf-8':
        fr = open(file_path, 'r', encoding="utf-8")
        in_data = fr.read()
    elif detected.get('encoding') == 'GB2312':
        try:
            fr = open(file_path, 'r', encoding="gbk")
            in_data = fr.read()
        except UnicodeDecodeError:
            fr = open(file_path, 'r', encoding="utf-8")
            in_data = fr.read()
    elif detected.get('encoding') == 'UTF-8-SIG':
        fr = open(file_path, 'r', encoding="UTF-8-SIG")
        in_data = fr.read()
    elif detected.get('encoding') == 'UTF-16':
        fr = open(file_path, 'r', encoding="UTF-16")
        in_data = fr.read()
    else:
        in_data = "error"
    return in_data


def main(in_path, out_path):
    # print("\n=================== pystart ===================")
    print("\npystart...")
    print('in_path:' + in_path)
    print('out_path:' + out_path)
    in_data = read_data(in_path)
    print(in_data)
    if in_data == 'error':
        print('this is an error about %s' % in_path)
    else:
        print('\nin_data:\n' + in_data)
        para_ners = nlp.analyse(in_data)
        out_data = ""
        type_name = ["date", "person", "location", "sentence"]
        for sentence_ners in para_ners:
            for i in range(len(sentence_ners)):
                out_data += type_name[i] + "|"
                for item in sentence_ners[i]:
                    out_data += item + "|"
                out_data += "\n"
        fw = open(out_path, 'w', encoding="utf-8")
        fw.write(out_data)
        fw.close()
        print(out_data)
        print("===============================================\n")


if __name__ == "__main__":
    files_path = ["./data" + '/' + x for x in os.listdir("./data")]
    for file_path in files_path:
        if os.path.splitext(file_path)[1] == '.txt':
            read_data(file_path)
