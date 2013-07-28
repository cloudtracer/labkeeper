from django.conf.urls import patterns, url

urlpatterns = patterns('scheduler',
    # Reservations
    url(r'^user/$', 'views.reservation_list', name='my_reservations'),
    url(r'^user/(?P<username>\w+)/$', 'views.reservation_list', name='reservation_list_user'),
    url(r'^(?P<rsv_id>\d+)/$', 'views.reservation', name='scheduler_reservation'),
    url(r'^(?P<rsv_id>\d+)/delete/$', 'views.delete_reservation', name='scheduler_delete_reservation'),
)
