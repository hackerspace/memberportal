from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView
from django.views.generic.simple import redirect_to
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from baseprofile.decorators import member_required

admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('',
    (r'^accounts/', include('simple_captcha_backend.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/profile/$',
        login_required(TemplateView.as_view(template_name="profile.html")),
        name='auth_profile'),
    url(r'^accounts/profile/edit/$',
        'baseprofile.views.edit',
        name='auth_profile_edit'),

    url(r'^accounts/members/$',
        'baseprofile.views.overview',
        name='members'),

    url(r'^accounts/members/list/$',
        login_required(member_required(ListView.as_view(
            queryset=User.objects.filter(
                baseprofile__status='AC').order_by('username'),
            template_name="member_list.html"))),
        name='members_list'),

    url(r'^accounts/members/list/accepted/$',
        login_required(member_required(ListView.as_view(
            queryset=User.objects.filter(
                baseprofile__status='AC').order_by('username'),
            template_name="member_list.html"))),
        name='members_list_accepted'),

    url(r'^accounts/members/list/rejected/$',
        login_required(member_required(ListView.as_view(
            queryset=User.objects.filter(
                baseprofile__status='RE').order_by('username'),
            template_name="member_list.html"))),
        name='members_list_rejected'),

    url(r'^accounts/members/list/awaiting/$',
        login_required(member_required(ListView.as_view(
            queryset=User.objects.filter(
                baseprofile__status='NA').order_by('username'),
            template_name="member_list.html"))),
        name='members_list_awaiting'),

    url(r'^accounts/members/list/ex/$',
        login_required(member_required(ListView.as_view(
            queryset=User.objects.filter(
                baseprofile__status='EX').order_by('username'),
            template_name="member_list.html"))),
        name='members_list_ex'),

    url(r'^payments/$',
        'payments.views.overview',
        name='payments'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/$', redirect_to, {'url' : '/accounts/profile/'}),
    url(r'^$', redirect_to, {'url' : '/accounts/profile/'}),
)
