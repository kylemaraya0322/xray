# diagnosis/templatetags/percent_extras.py

from django import template

register = template.Library()

@register.filter
def to_percentage(value, decimals=2):
    """
    Multiplies a 0–1 float by 100 and formats with `decimals` places.
    Usage: {{ value|to_percentage }}  → "83.37%"
           {{ value|to_percentage:1 }} → "83.4%"
    """
    try:
        pct = float(value) * 100
        return f"{pct:.{int(decimals)}f}%"
    except (ValueError, TypeError):
        return ''
