from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'labkeeper.views.default', name='home'),

    # Native apps
    url(r'^labs/', include('labs.urls')),
    url(r'^reservations/', include('scheduler.urls')),

    # TinyMCE
    url(r'^tinymce/', include('tinymce.urls')),

    # Admin interface
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
