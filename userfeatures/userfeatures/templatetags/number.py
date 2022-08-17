from django import template

register = template.Library()


import math

multiplier = [
    (0, ''),
    (3, 'k'),
    (6, 'm'),
]


@register.filter()
def short_number(a, b):
    number = a - int(b)

    s = number
    n = ''

    if number > 1000000:
        s =  number // 1000000
        n = 'm'

    if number > 1000:
        s = number // 1000
        n = 'k'

    return f"{s}{n}"

