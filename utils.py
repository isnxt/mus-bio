def format_data(str):
    str = str.replace("。", "。|")
    data = str.split('|')
    return data

def get_tagword(ners):
    list_person = []
    list_location = []
    list_time = []
    for ner in ners:
        word = ner[0]
        tag = ner[1]
        if tag == 'PERSON':
            list_person.append(word)
        if tag == 'CITY' or  tag == 'COUNTRY':
            list_location.append(word)
        if tag == 'DATE':
            list_time.append(word)
    return list_person, list_location, list_time