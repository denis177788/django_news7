from django import template
from ..models import Post


register = template.Library()


word_list = ['редиска', 'режим', 'союз', 'библиотека', 'засуха']


# Возвращает тип поста: "Новость" или "Статья"
@register.filter()
def type_filter(value):
    for a in Post.POSITIONS:
        if a[0] == value:
            return a[1]
    return None


@register.filter()
def censor(value):

    def check_word(word):
        for j in range(0, len(word_list)):
            if word.lower() == word_list[j]:
                # есть совпадение - цензурируем!
                new_word = word[0]
                for k in range(1, len(word)):
                    new_word += '*'
                word = new_word
        return word

    if type(value) != str:
        return 'Ошибка: "value" не строка!'

    s = ''
    i = 0
    new_word = ''

    while i < len(value):
        c = value[i]
        if (c != ' ') and (c != '.') and (c != ',') and (c != '!') and (c != '?') and (c != ' '):
            new_word += c
        else:
            # print('new_word='+new_word)
            if new_word != '':
                s = s + check_word(new_word) + c
                new_word = ''
            else:
                s += c
        i += 1
    if new_word != '':
        s = s + check_word(new_word)
    return s
