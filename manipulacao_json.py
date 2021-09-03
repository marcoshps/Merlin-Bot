import json


def write_json(words, file):
    with open(file, 'w') as f:
        json.dump(words, f, ensure_ascii=False, indent=4)


def loadJson(file):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def dict_to_binary(the_dict):
    string = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in string)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    reverse = json.loads(jsn)
    return reverse
