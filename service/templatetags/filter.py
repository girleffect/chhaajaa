from django import template
register = template.Library()

@register.filter
def integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False