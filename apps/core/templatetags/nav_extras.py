from django import template


register = template.Library()


@register.filter
def startswith(value, prefix):
    try:
        return str(value).startswith(str(prefix))
    except Exception:
        return False

