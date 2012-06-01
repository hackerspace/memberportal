from django import template

from payments.common import payments_by_month

register = template.Library()

@register.filter
def format_payment(inp):
    out = ''
    for spec in inp:
        if 'month2' in spec:
            out += '%s/%s-%s ' % (spec['year'], spec['month'], spec['month2'])
        else:
            out += '%s/%s ' % (spec['year'], spec['month'])

    return out

@register.filter
def cal_generator(inp):
    return payments_by_month(inp)
