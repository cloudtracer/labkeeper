from django.conf.urls import patterns, url

urlpatterns = patterns('labs',
    url(r'^$', 'views.default', name='labs'),
    url(r'^(?P<lab_id>\d+)/$', 'views.lab', name='lab'),
    url(r'^(?P<lab_id>\d+)/manage/profile/$', 'views.manage_profile', name='labs_manage_profile'),
    url(r'^(?P<lab_id>\d+)/manage/devices/$', 'views.manage_devices', name='labs_manage_devices'),
    url(r'^(?P<lab_id>\d+)/manage/pods/$', 'views.manage_pods', name='labs_manage_pods'),
    url(r'^(?P<lab_id>\d+)/manage/consoleservers/$', 'views.manage_consoleservers', name='labs_manage_consoleservers'),
    url(r'^pods/(?P<pod_id>\d+)/delete/$', 'views.delete_pod', name='labs_delete_pod'),
    url(r'^consoleservers/(?P<cs_id>\d+)/delete/$', 'views.delete_consoleserver', name='labs_delete_consoleserver'),
)
