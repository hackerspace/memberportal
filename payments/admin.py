from django.contrib import admin

from models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'payment_type',
    'variable_symbol', 'identification', 'message',
    'correction_required', 'parsed', 'user_not_none',)

    list_editable = ('correction_required', 'parsed',)
    list_filter = ('correction_required',)

    def user_not_none(self, obj):
        if obj.user is None:
            return ''
        return '%s' % obj.user
    user_not_none.short_description = 'User'



admin.site.register(Payment, PaymentAdmin)
