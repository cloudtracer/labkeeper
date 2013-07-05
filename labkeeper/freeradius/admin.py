from django.contrib import admin

from freeradius.models import *


class RadcheckAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'op', 'value')

class RadreplyAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'op', 'value')


admin.site.register(Radcheck, RadcheckAdmin)
admin.site.register(Radreply, RadreplyAdmin)
