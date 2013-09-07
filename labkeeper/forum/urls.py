from django.conf.urls import patterns, url

urlpatterns = patterns('forum',

    # Forum list
    url(r'^$', 'views.default', name='forum'),

    # Forum
    url(r'^(?P<forum_slug>[-\w]+)/$', 'views.forum', name='forum_forum'),

    # Topic
    url(r'^topic/(?P<topic_id>\d+)/$', 'views.topic', name='forum_topic'),
    url(r'^(?P<forum_slug>[-\w]+)/new/$', 'views.new_topic', name='forum_new_topic'),

    # Post
    url(r'^post/(?P<post_id>\d+)/edit/$', 'views.edit_post', name='forum_edit_post'),

)
