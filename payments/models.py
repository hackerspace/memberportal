from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from fio import msg_parser

class Payment(models.Model):
    user = models.ForeignKey(User,
        blank = True,
        null = True)

    date = models.DateField(
        verbose_name = _('Payment arrival'))

    amount = models.FloatField(
        verbose_name = _('Payment amount'))

    payment_type = models.CharField(
        max_length = 200,
        blank = True,
        verbose_name = _('Type'))

    constant_symbol = models.IntegerField(
        blank = True,
        null = True)

    variable_symbol = models.IntegerField(
        blank = True,
        null = True)

    specific_symbol = models.IntegerField(
        blank = True,
        null = True)

    identification = models.CharField(
        max_length = 200,
        blank = True,
        verbose_name = _('Identification'))

    message = models.CharField(
        max_length = 200,
        blank = True,
        verbose_name = _('Message'))

    parsed = models.CharField(
        max_length = 200,
        blank = True,
        verbose_name = _('Corrected message'))

    correction_required = models.BooleanField(
        default = False,
        verbose_name = _('Correction required'))

    def __unicode__(self):
        return '%s (%s CZK)' % (self.date, self.amount)

    def parse(self):
        try:
            return msg_parser.parse_message(self.parsed)
        except msg_parser.MessageSyntaxError:
            return None

    def formonths(self):
        '''
        Returns sorted dict with (year, month) tuples
        E.g.: [(2011, 1), ... , (2011, 12), (2012, 1)]
        '''
        parsed = self.parse()
        if parsed is None:
            return []

        ret = []
        for spec in parsed:
            if 'month2' in spec:
                for month in range(spec['month'], spec['month2']+1):
                    ret.append((spec['year'], month))
            else:
                ret.append((spec['year'], spec['month']))

        return sorted(ret)

    class Meta:
        ordering = ('-date', )

def parse_payment_message(sender, instance, created, raw, **kwargs):
    if not created or raw:
        return

    try:
        parsed = msg_parser.parse_message(instance.message)
        if parsed == []:
            instance.parsed = '%s/%s' % (instance.date.year,
                instance.date.month)
        else:
            instance.parsed = instance.message
    except msg_parser.MessageSyntaxError:
        instance.correction_required = True

    instance.save()

post_save.connect(parse_payment_message, sender=Payment)
