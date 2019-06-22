# Musician Biography 

## 1.数据搜集
### 目录说明
- NLP-zh/data/wiki：所有wiki音乐家生平输入txt
- NLP-zh/out/xx.csv：融合xx个wiki音乐家的csv
- NLP-zh/data/clean_5/done：每个wiki音乐家生平输出csv(不含无法识别地点)
- NLP-zh/data/clean_5/：每个wiki音乐家生平输出csv(去掉无法识别地点)



## 2.实时输出
### 目录说明
- NLP-zh/data/wiki：所有wiki音乐家生平输入txt
### 运行步骤
- 下载 https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip  
把解压到某路径下 举例：E:\stanford-corenlp-full-2018-10-05
- 下载 https://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-10-05-models.jar  
放到刚才解压后的文件夹stanford-corenlp-full-2018-10-05下
- 将start.bat放到刚才解压后的文件夹stanford-corenlp-full-2018-10-05下，并运行
- 调用py2java.py

