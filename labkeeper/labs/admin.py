from django.contrib import admin

from labs.models import Lab, Pod, ConsoleServer, Device


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public')


class PodAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab')


class ConsoleServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pod')


admin.site.register(Lab, LabAdmin)
admin.site.register(Pod, PodAdmin)
admin.site.register(ConsoleServer, ConsoleServerAdmin)
admin.site.register(Device, DeviceAdmin)
