from django import template

register = template.Library()

@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')