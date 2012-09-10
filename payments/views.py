from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import Payment
from baseprofile.decorators import member_required

@login_required
@member_required
def overview(request, template_name='finance.html'):
    payments = Payment.objects.all()

    balance = 0
    for payment in payments:
        balance += payment.amount

    data = {
        'balance': balance,
        'payments': payments,
    }

    return render_to_response(template_name, data,
        context_instance=RequestContext(request))
