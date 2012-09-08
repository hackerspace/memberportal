from datetime import date

class YearInfo(object):
    def __init__(self, year, months_ok, months_na):
        self.year = year
        self.months = set(range(1, 13))
        self.months_ok = set(months_ok)
        self.months_na = set(months_na)
        self.months_er = self.months - (self.months_ok | self.months_na)

        today = date.today()
        if self.year == today.year:
            self.months_er -= set(range(today.month, 13))

    def __unicode__(self):
        return u'%s' % self.year

    def missing(self):
        return len(self.months_er) != 0

def payments_by_month(payments_list):
    monthly_data = set()
    if not payments_list:
        return []

    for payment in payments_list:
        for m in payment.formonths():
            monthly_data.add(m)
    since_year = payment.user.date_joined.year
    since_month = payment.user.date_joined.month

    years = set(range(since_year, date.today().year+1))

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

def no_missing_payments(payments_list):
    plist = payments_by_month(payments_list)
    for year in plist:
         if year.missing():
             return False

    return True

def missing_months(payments_list):
    plist = payments_by_month(payments_list)
    missing = []
    for yi in plist:
        if yi.missing():
            for month in yi.months_er:
                missing.append((yi.year, month))

    return missing
