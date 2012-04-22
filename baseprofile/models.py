from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

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
        verbose_name = _('ID used for payments'),
        help_text = _('Variable symbol'))

    def __unicode__(self):
        return '%s\'s profile' % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        BaseProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
