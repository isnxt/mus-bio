from stanfordcorenlp import StanfordCoreNLP
import utils
import os

module_path = os.path.dirname(__file__)


class NLP:
    def __init__(self):
        # Use an existing server
        self.model = StanfordCoreNLP('http://localhost', port=9000, lang='zh')

    def close(self):
        self.model.close()

    def get_ner(self, sentence):
        return self.model.ner(sentence)


