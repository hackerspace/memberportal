from django.conf import settings
from django.core.mail import mail_managers
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from models import BaseProfile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pids = BaseProfile.objects.all().values_list('payments_id')
        obj = BaseProfile(user=instance)
        if pids:
            next_id = sorted(pids)[-1][0]
            obj.payments_id = next_id + 1
        obj.save()

def send_mail_if_status_changed(sender, instance, **kwargs):
    try:
        obj = BaseProfile.objects.get(pk=instance.pk)
    except BaseProfile.DoesNotExist:
        # New object
        subject = _('New user registered')
        message = _('New membership request: %s, %s') % (instance.user.username,
            instance.user.email)
        mail_managers(subject, message)
    else:
        if not obj.status == instance.status:
            subject = _('Membership status change')
            message = _('Your status have changed from "%s" to "%s"') % (
                obj.get_status_display(), instance.get_status_display())
            if instance.user.email:
                instance.user.email_user(subject, message)

def enable():
    post_save.connect(create_user_profile, sender=User)

    if getattr(settings, 'MEMBER_STATUS_EMAIL_NOTIFY', False) == True:
        pre_save.connect(send_mail_if_status_changed, sender=BaseProfile)
