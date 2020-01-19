from django import template
from collections import OrderedDict

register = template.Library()

@register.filter(name='sort_dict_by_key')
def sort_dict_by_key(value):
    if isinstance(value, dict):
        new_dict = OrderedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        return sorted(value)
    else:
        return value
    listsort.is_safe = True