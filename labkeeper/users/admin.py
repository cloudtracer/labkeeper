from django.contrib import admin

from users.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country')


admin.site.register(UserProfile, UserProfileAdmin)
