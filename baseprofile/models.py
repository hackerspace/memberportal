from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from payments.common import has_paid_until

class BaseProfile(models.Model):
    user = models.OneToOneField(User)

    alt_nick = models.CharField(
        max_length = 100,
        blank = True,
        verbose_name = _('Alternative nick'))

    phone = models.CharField(
        max_length = 20,
        blank = True,
        verbose_name = _('Phone number'))

    xmpp  = models.CharField(
        max_length = 200,
        blank = True,
        verbose_name = _('Jabber ID'))

    accepted = models.BooleanField(
        default = False,
        verbose_name = _('Accepted as a member'))

    council = models.BooleanField(
        default = False,
        verbose_name =  _('Member of the council'))

    revision = models.BooleanField(
        default = False,
        verbose_name = _('Member of the revision committee'))

    payments_id = models.PositiveSmallIntegerField(
        default = 0,
        unique = True,
        verbose_name = _('ID used for payments'),
        help_text = _('Variable symbol'))

    def __unicode__(self):
        return '%s\'s profile' % self.user

    def paid(self):
        till = date.today() - timedelta(days=30)
        return has_paid_until(self.user.payment_set.all(), till.year,
            till.month)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pids = BaseProfile.objects.all().values_list('payments_id')
        obj = BaseProfile(user=instance)
        if pids:
            next_id = sorted(pids)[-1][0]
            obj.payments_id = next_id + 1
        obj.save()

post_save.connect(create_user_profile, sender=User)
