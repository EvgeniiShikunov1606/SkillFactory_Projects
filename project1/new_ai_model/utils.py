import re


def normalize_word(word):
    # Замена спецсимволов на текст (необходимо ли?)
    word = re.sub(r'[1!|]', 'i', word)
    word = re.sub(r'[0]', 'o', word)
    word = re.sub(r'[6]', 'b', word)
    return word
