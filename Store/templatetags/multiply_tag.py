from django import template

register = template.Library()


@register.simple_tag
def multiply(value, value2):
    return str(round(float(value) * float(value2), 2))