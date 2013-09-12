from django.conf.urls import patterns, url

urlpatterns = patterns('labs',
    # Lab list
    url(r'^$', 'views.default', name='labs'),

    # Lab creation
    url(r'^new/$', 'views.create_lab', name='labs_create_lab'),

    # Lab info
    url(r'^(?P<lab_id>\d+)/$', 'views.lab', name='labs_lab'),
    url(r'^(?P<lab_id>\d+)/schedule/$', 'views.schedule', name='labs_schedule'),
    url(r'^(?P<lab_id>\d+)/members/$', 'views.member_list', name='labs_member_list'),
    url(r'^(?P<lab_id>\d+)/activity/$', 'views.recent_activity', name='labs_recent_activity'),

    # Lab/device management
    url(r'^(?P<lab_id>\d+)/edit/$', 'views.edit_lab_profile', name='labs_edit_lab_profile'),
    url(r'^(?P<lab_id>\d+)/settings/$', 'views.edit_lab_settings', name='labs_edit_lab_settings'),
    url(r'^(?P<lab_id>\d+)/manage/topologies/$', 'views.manage_topologies', name='labs_manage_topologies'),
    url(r'^(?P<lab_id>\d+)/manage/devices/$', 'views.manage_devices', name='labs_manage_devices'),
    url(r'^(?P<lab_id>\d+)/manage/pods/$', 'views.manage_pods', name='labs_manage_pods'),
    url(r'^(?P<lab_id>\d+)/manage/consoleservers/$', 'views.manage_consoleservers', name='labs_manage_consoleservers'),
    url(r'^(?P<lab_id>\d+)/delete/$', 'views.delete_lab', name='labs_delete_lab'),
    url(r'^topologies/(?P<topology_id>\d+)/delete/$', 'views.delete_topology', name='labs_delete_topology'),
    url(r'^pods/(?P<pod_id>\d+)/edit/$', 'views.edit_pod', name='labs_edit_pod'),
    url(r'^pods/(?P<pod_id>\d+)/delete/$', 'views.delete_pod', name='labs_delete_pod'),
    url(r'^consoleservers/(?P<cs_id>\d+)/edit/$', 'views.edit_consoleserver', name='labs_edit_consoleserver'),
    url(r'^consoleservers/(?P<cs_id>\d+)/delete/$', 'views.delete_consoleserver', name='labs_delete_consoleserver'),
    url(r'^devices/(?P<device_id>\d+)/edit/$', 'views.edit_device', name='labs_edit_device'),
    url(r'^devices/(?P<device_id>\d+)/delete/$', 'views.delete_device', name='labs_delete_device'),

    # Membership invitations
    url(r'^invitations/(?P<invitation_id>\d+)/(?P<response>accept|decline)/$', 'views.invitation_response', name='labs_invitation_response'),

)
