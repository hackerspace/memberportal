from django.contrib import admin

from models import BaseProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'accepted', 'council', 'revision', 'payments_id',)

admin.site.register(BaseProfile, ProfileAdmin)
