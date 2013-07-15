from django.conf.urls import patterns, url

urlpatterns = patterns('labs',
    # Lab list
    url(r'^$', 'views.default', name='labs'),

    # Lab info
    url(r'^(?P<lab_id>\d+)/$', 'views.lab', name='lab'),
    url(r'^(?P<lab_id>\d+)/schedule/$', 'views.schedule', name='labs_schedule'),
    url(r'^(?P<lab_id>\d+)/members/$', 'views.member_list', name='labs_member_list'),

    # Lab/device management
    url(r'^(?P<lab_id>\d+)/manage/profile/$', 'views.manage_lab', name='labs_manage_lab'),
    url(r'^(?P<lab_id>\d+)/manage/devices/$', 'views.manage_devices', name='labs_manage_devices'),
    url(r'^(?P<lab_id>\d+)/manage/pods/$', 'views.manage_pods', name='labs_manage_pods'),
    url(r'^(?P<lab_id>\d+)/manage/consoleservers/$', 'views.manage_consoleservers', name='labs_manage_consoleservers'),
    url(r'^pods/(?P<pod_id>\d+)/delete/$', 'views.delete_pod', name='labs_delete_pod'),
    url(r'^consoleservers/(?P<cs_id>\d+)/edit/$', 'views.edit_consoleserver', name='labs_edit_consoleserver'),
    url(r'^consoleservers/(?P<cs_id>\d+)/delete/$', 'views.delete_consoleserver', name='labs_delete_consoleserver'),
)
