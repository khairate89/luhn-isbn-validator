from django import template

register = template.Library()

@register.filter
def is_even(value):
    """Return True if the number is even."""
    try:
        return int(value) % 2 == 0
    except (ValueError, TypeError):
        return False
