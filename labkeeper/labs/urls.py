from django.conf.urls import patterns, url

urlpatterns = patterns('labs',
    url(r'^$', 'views.default', name='labs'),
    url(r'^(?P<id>\d+)/$', 'views.lab', name='lab'),
    url(r'^(?P<id>\d+)/manage/profile/$', 'views.manage_profile', name='labs_manage_profile'),
    url(r'^(?P<id>\d+)/manage/devices/$', 'views.manage_devices', name='labs_manage_devices'),
    url(r'^(?P<id>\d+)/manage/pods/$', 'views.manage_pods', name='labs_manage_pods'),
    url(r'^pods/(?P<id>\d+)/delete/$', 'views.delete_pod', name='labs_delete_pod'),
)
