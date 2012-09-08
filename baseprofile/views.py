from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forms import ProfileForm
from models import BaseProfile

@login_required
def edit(request, template_name='edit_profile.html',
    redirect_to='auth_profile'):

    form = ProfileForm(request.POST, instance=request.user.get_profile())
    if request.POST:
        if form.is_valid():
            form.save()
            u = request.user
            u.email = form.data['email']
            u.first_name = form.data['first_name']
            u.last_name = form.data['last_name']
            u.save()
        else:
            return render_to_response(template_name, {'form': form},
                context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse(redirect_to))

    else:
        initial_dict = {'email': request.user.email,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name}

        form = ProfileForm(instance=request.user.get_profile(),
            initial=initial_dict)

        return render_to_response(template_name, {'form': form},
            context_instance=RequestContext(request))

@login_required
def overview(request, template_name='members.html'):
    members  = set(BaseProfile.members.all())
    awaiting = BaseProfile.awaiting.all()
    ex       = BaseProfile.ex.all()
    rejected = BaseProfile.rejected.all()

    paying = set(filter(lambda x: x.paid(), members))
    not_paying = members - paying

    lists = {
        'paying': paying,
        'not_paying': not_paying,
        'members': members,
        'awaiting': awaiting,
        'ex': ex,
        'rejected': rejected,
    }

    data = {}
    for key, value in lists.items():
        data[key] = map(lambda x: x.user, value)

    return render_to_response(template_name, data,
        context_instance=RequestContext(request))
