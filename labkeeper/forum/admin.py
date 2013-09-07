from django.contrib import admin

from forum.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')


class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'position', 'description')
    ordering = ['category__position', 'position']


class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'forum', 'created', 'author', 'sticky', 'closed')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'author', 'created', 'updated')
    ordering = ['-created']
    readonly_fields = ['author', 'author_ip']




admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
