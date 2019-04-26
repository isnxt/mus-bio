import model
import utils
import sys


nlp_model = model.NLP()


def init():
    print("init model...")
    nlp_model.init()


def close():
    nlp_model.close()


def analyse(str_input):
    print("analysing...")

    sentences = utils.format_data(str_input)
    results = []
    for sentence in sentences:
        if sentence != "":
            ners = nlp_model.get_ner(sentence)
            pers, locs, tims = utils.get_tagword(ners)
            results.append([pers, locs, tims, [sentence]])
    return results


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    print(input_path)
    print(output_path)
    init()
    file = open(input_path, 'r', encoding="utf-8")
    data = file.read()
    print('data:\n', data)
    sentences_ner = analyse(data)
    with open(output_path, 'w') as f:
        for sentence_ner in sentences_ner:
            for ner in sentence_ner:
                for item in ner:
                    f.write("%s|" % item)
                f.write("\n")
    close()
    print("python end ...\n\n")


