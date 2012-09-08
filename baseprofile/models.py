from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from payments.common import has_paid_until

MEMBERSHIP_STATES = (
    ('NA', 'Awaiting'),
    ('AC', 'Accepted'),
    ('RE', 'Rejected'),
    ('EX', 'Ex-member')
)

class MemberManager(models.Manager):
    def __init__(self, status, *args, **kwargs):
        self.status = status
        super(MemberManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        return super(MemberManager, self).get_query_set().filter(
            status=self.status)

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

    status = models.CharField(
        max_length = 2,
        default = 'NA',
        choices=MEMBERSHIP_STATES)

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
        users_payments = self.user.payment_set.all()
        if not users_payments:
            return False

        return has_paid_until(users_payments, till.year,
            till.month)

    def accepted(self):
        return self.status == 'AC'

    objects  = models.Manager()
    members  = MemberManager('AC')
    awaiting = MemberManager('NA')
    rejected = MemberManager('RE')
    ex       = MemberManager('EX')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pids = BaseProfile.objects.all().values_list('payments_id')
        obj = BaseProfile(user=instance)
        if pids:
            next_id = sorted(pids)[-1][0]
            obj.payments_id = next_id + 1
        obj.save()

post_save.connect(create_user_profile, sender=User)
