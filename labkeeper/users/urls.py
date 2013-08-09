from django.conf.urls import patterns, url

urlpatterns = patterns('users',
    #url(r'^$', 'views.default', name='users'),

    # Login/logout
    url(r'^login/$', 'views.login', name='login'),
    url(r'^logout/$', 'views.logout', name='logout'),

    # User profiles
    url(r'^(?P<username>\w+)/$', 'views.profile', name='users_profile'),
    url(r'^(?P<username>\w+)/edit/$', 'views.edit_profile', name='users_edit_profile'),
)
