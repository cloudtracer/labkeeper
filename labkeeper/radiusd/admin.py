from django.contrib import admin

from radiusd.models import RadiusLogin


class RadiusLoginAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_display = ('time', 'device', 'user', 'user_ip')
    list_filter = ('time',)
    readonly_fields = RadiusLogin._meta.get_all_field_names()

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(RadiusLogin, RadiusLoginAdmin)
