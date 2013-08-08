from django.conf.urls import patterns, url

urlpatterns = patterns('users',
    #url(r'^$', 'views.default', name='users'),

    # Lab/device management
    url(r'^(?P<username>\w+)/$', 'views.profile', name='users_profile'),
)
