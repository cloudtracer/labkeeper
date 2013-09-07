from django.conf.urls import patterns, include, static, url
from django.contrib import admin
import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'labkeeper.views.home', name='home'),

    # Native apps
    url(r'^forum/', include('forum.urls')),
    url(r'^labs/', include('labs.urls')),
    url(r'^reservations/', include('scheduler.urls')),
    url(r'^users/', include('users.urls')),

    # TinyMCE
    url(r'^tinymce/', include('tinymce.urls')),

    # Admin interface
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
