from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'labs.views.default', name='labs'),
)
