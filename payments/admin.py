from django.contrib import admin

from models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'payment_type', 
    'constant_symbol', 'variable_symbol', 'specific_symbol', 
    'identification', 'message', 'parsed', 'user')

admin.site.register(Payment, PaymentAdmin)
