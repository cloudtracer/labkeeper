from django.conf.urls import patterns, url

urlpatterns = patterns('labs',
    url(r'^$', 'views.default', name='labs'),
    url(r'^(?P<id>\d+)/$', 'views.lab', name='lab'),
    url(r'^edit/(?P<id>\d+)/$', 'views.lab_edit', name='lab_edit'),
)
