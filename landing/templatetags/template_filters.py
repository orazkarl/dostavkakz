from django import template

register = template.Library()


@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)


@register.filter
def multiply(string, times):
    return string * times


@register.filter()
def range(min, max):
    # print(min)
    return range(int(max))
