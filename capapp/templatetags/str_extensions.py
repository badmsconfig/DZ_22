from django import template

register = template.Library()

def capitalize(inputstr):
    return inputstr.capitalize()

def superoutput(inputstr):
    # ГлавНая страница
    # ГлАвНаЯ СтРаНиЦа
    result = []
    for i in range(len(inputstr)):
        letter = inputstr[i]
        if i % 2 != 0:
            letter = letter.upper()
        result.append(letter)
    return ''.join(result)

register.filter('capitalize', capitalize)
register.filter('sup', superoutput)