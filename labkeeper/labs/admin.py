from django.contrib import admin

from labs.models import Lab, Pod, Device, ConsoleServer, ConsoleServerPort


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public')


class PodAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pod', 'port')


class ConsoleServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab', 'fqdn', 'ip4_address')


class ConsoleServerPortAdmin(admin.ModelAdmin):
    list_display = ('consoleserver', 'number', 'device', 'telnet_port', 'ssh_port')


admin.site.register(Lab, LabAdmin)
admin.site.register(Pod, PodAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(ConsoleServer, ConsoleServerAdmin)
admin.site.register(ConsoleServerPort, ConsoleServerPortAdmin)
