from django.contrib import admin

from models import BaseProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'status', 'council', 'revision', 'payments_id',)
    list_editable = ('status', )

admin.site.register(BaseProfile, ProfileAdmin)
