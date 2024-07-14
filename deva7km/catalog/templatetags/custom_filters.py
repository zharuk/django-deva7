# seller_cabinet/templatetags/custom_filters.py
from django import template
from django.utils.dateformat import DateFormat

register = template.Library()


@register.filter
def format_date(value):
    return DateFormat(value).format('d M Y H:i:s')
