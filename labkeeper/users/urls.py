from django.conf.urls import patterns, url

urlpatterns = patterns('users',
    #url(r'^$', 'views.default', name='users'),

    # User profiles
    url(r'^(?P<username>\w+)/$', 'views.profile', name='users_profile'),
    url(r'^(?P<username>\w+)/edit/$', 'views.edit_profile', name='users_edit_profile'),
)
