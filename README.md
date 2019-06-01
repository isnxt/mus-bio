# Musician Biography 

## Python Part 说明
### 运行前准备
- 下载 https://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip  
把解压到某路径下 举例：E:\stanford-corenlp-full-2018-10-05
- 下载 https://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-10-05-models.jar  
放到刚才解压后的文件夹stanford-corenlp-full-2018-10-05下
- 将start.bat放到刚才解压后的文件夹stanford-corenlp-full-2018-10-05下，并运行
- 打开JDemo工程，修改Main.java三个path的设置（绝对路径）
- 运行Main.java即可

### 目录说明
- JDemo：java example project to use python model
- NLP-zh：python project
- NLP-zh/data/wiki-life：可用来作为测试输入的所有wiki音乐家生平txt
- NLP-zh/out/wiki-life：所有wiki音乐家生平的测试输出
### Python输出格式
.txt
```
第1行：第1句话的时间列表，以‘|’分隔
第2行：第1句话的人物列表，以‘|’分隔
第3行：第1句话的地点列表，以‘|’分隔
第4行：第1句话的事情列表，以‘|’分隔
第5行：第2句话的时间列表，以‘|’分隔
第6行：第2句话的人物列表，以‘|’分隔
第7行：第2句话的地点列表，以‘|’分隔
第8行：第2句话的事情列表，以‘|’分隔
...
```
### Python功能
[基本功能] 
- 中文分句
- 识别一般的时间/地点/人物实体

[补充功能] 
- 排除引号|书名号|括号对实体识别的干扰
- 中文数字格式的时间实体>>阿拉伯数字格式
- 补全缺失年的时间实体
- 岁数>>年格式
- 按照','隔离划分含有多个时间实体的句子, 如果按照','划分后仍有多个时间实体：     
a. 如果年相同，只返回年 b. 如果年不同，返回min年-max年     

### wiki 音乐家

