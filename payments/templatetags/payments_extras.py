from datetime import date

from django import template

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

class YearInfo(object):
    def __init__(self, year, months_ok, months_na):
        self.year = year
        self.months = set(range(1, 13))
        self.months_ok = set(months_ok)
        self.months_na = set(months_na)
        self.months_er = self.months - (self.months_ok | self.months_na)

        today = date.today()
        if self.year == today.year:
            print self.months_er
            self.months_er -= set(range(today.month, 13))
            print self.months_er

    def __unicode__(self):
        return u'%s' % self.year

@register.filter
def cal_generator(inp):
    years = set()
    monthly_data = set()
    if not inp:
        return []

    for payment in inp:
        for m in payment.formonths():
            years.add(m[0])
            monthly_data.add(m)
    since_year = payment.user.date_joined.year
    since_month = payment.user.date_joined.month
    years.add(since_year)

    out = []
    for y in years:
        ok = map(lambda x: x[1],
            filter(lambda x: x[0] == y, monthly_data))

        na = []
        if y == since_year:
            na = range(1, since_month)

        yi = YearInfo(y, ok, na)

        out.append(yi)
    return out

