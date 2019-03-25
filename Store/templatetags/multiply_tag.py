from django import template

register = template.Library()


@register.simple_tag
def multiply(value, value2):
    return str(float(value) * float(value2))