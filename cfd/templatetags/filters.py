import datetime
from django import template

register = template.Library()

@register.filter
def get_field_data(form, field):
    field = form.fields[field].get_bound_field(form, field)

    return {
        'name' : field.name,
        'label_tag' : field.label_tag(),
        'field' : field,
        'help_text' : field.help_text
    }    

@register.filter
def get_index(array, index):
    try:
        return array[index]
    except IndexError:
        return None


@register.filter
def get_key(dictionary, key):
    return dictionary.get(key, "")
