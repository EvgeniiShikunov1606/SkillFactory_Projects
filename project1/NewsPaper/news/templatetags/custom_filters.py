from django import template
import re

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}

forbidden_words = ['сука']


@register.filter()
def currency(value, code='rub'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'


@register.filter(name='censor')
def censor(value, bad_words):
    bad_words_list = bad_words.split(',')

    def replace_word(word):
        return word[0] + '*' * (len(word) - 1)

    for word in bad_words_list:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        value = pattern.sub(replace_word(word), value)

    return value


@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*" * (len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

