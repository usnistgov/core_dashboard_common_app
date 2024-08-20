""" Core dashboard tag to pluralize labels
FIXME: temporary solution, need to update the template and constant system to deal with singular/plural
"""

from django import template

register = template.Library()


@register.filter(name="special_plural")
def special_case_plural(value):
    """special_case_plural

    Args:
        value:

    Returns:
    """
    if value.endswith("y"):
        return value.replace("y", "ies")
    return f"{value}s"
