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
    # url(r'^$', 'fu.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name}}.foo.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/profile/$', login_required(TemplateView.as_view(
        template_name="profile.html"))),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', redirect_to, {'url' : '/accounts/profile/'}),
)
