from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.simple import redirect_to
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$',
        login_required(TemplateView.as_view(template_name="profile.html")),
        name='auth_profile'),
    url(r'^accounts/profile/edit/$',
        'baseprofile.views.edit',
        name='auth_profile_edit'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', redirect_to, {'url' : '/accounts/profile/'}),
)
