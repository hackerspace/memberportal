from django.contrib.auth.models import User
from django.db.models.signals import post_save

from models import BaseProfile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pids = BaseProfile.objects.all().values_list('payments_id')
        obj = BaseProfile(user=instance)
        if pids:
            next_id = sorted(pids)[-1][0]
            obj.payments_id = next_id + 1
        obj.save()

def enable():
    post_save.connect(create_user_profile, sender=User)
