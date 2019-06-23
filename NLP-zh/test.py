# -*- coding: utf-8
import os
import py2java
from core import utils

root_path = os.path.abspath('.')
path_out = root_path + "\\out"
path_bat = root_path + "\\start.bat"

if not os.path.exists(path_out + "\\wiki"):
    os.mkdir(path_out + "\\wiki")


def test_all():
    utils.clean_folder(path_out + "\\wiki")
    files = os.listdir(root_path + "\\data\\wiki")
    for file in files:
        in_path = root_path + "\\data\\wiki\\" + file
        out_path = path_out + "\\wiki\\" + file
        py2java.main(in_path, out_path)


def test():
    file = "韋瓦第.txt"
    in_path = root_path + "\\data\\wiki\\" + file
    out_path = path_out + "\\" + file
    py2java.main(in_path, out_path)


def sample_test():
    file = "sample.txt"
    in_path = root_path + "\\data\\" + file
    out_path = path_out + "\\" + file
    py2java.main(in_path, out_path)


if __name__ == "__main__":
    test_all()
