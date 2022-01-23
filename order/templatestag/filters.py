from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter("iconbool", is_safe=True)
def iconbool(value):

    if bool(value):
        result = '<i class="bi bi-check-circle-fill text-success"></i>'
    else:
        result = '<i class="bi bi-x text-danger"></i>'
    return mark_safe(result)
