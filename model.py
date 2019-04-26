from stanfordcorenlp import StanfordCoreNLP
import os
import os

module_path = os.path.dirname(__file__)

class NLP:
    def init(self):
        self.nlp = StanfordCoreNLP(module_path + "/lib/stanford-corenlp-full-2018-02-27", lang='zh')

    def close(self):
        self.nlp.close()

    def get_ner(self, sentence):
        return self.nlp.ner(sentence)
