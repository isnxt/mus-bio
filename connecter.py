import model
import utils
import sys, os

module_path = os.path.dirname(__file__)


def analyse(str_input):
    print("\n-------------------analyse start-------------------")
    nlp_model = model.NLP()
    sentences = utils.format_data(str_input)
    para_ners = []
    for sentence in sentences:
        if sentence != "":
            print('\nsentence:\n', sentence)
            ners = nlp_model.get_ner(sentence)
            print('\nners:\n', ners)
            tims, pers, locs = utils.get_tagword(ners)
            if len(tims) != 0:
                para_ners.append([tims, pers, locs, [sentence]])
    nlp_model.close()
    print("\n-------------------analyse end-------------------")
    return para_ners


if __name__ == "__main__":
    print("\n-------------------python start-------------------")
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    # in_path = module_path + "/in.txt"
    # out_path = module_path + "/out.txt"
    print('\nin_path:\n' + in_path)
    print('\nout_path:\n' + out_path)
    fr = open(in_path, 'r', encoding="utf-8")
    in_data = fr.read()
    fr.close()
    print('\nin_data:\n' + in_data)
    para_ners = analyse(in_data)
    out_data = ""
    for sentence_ners in para_ners:
        for type_ner in sentence_ners:
            for item in type_ner:
                out_data += item + "|"
            out_data += "\n"
    fw = open(out_path, 'w', encoding="utf-8")
    fw.write(out_data)
    fw.close()
    print('\nout_data:\n' + out_data)

    print("\n-------------------python end-------------------\n\n")
