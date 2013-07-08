from django.contrib import admin

from labs.models import Lab, LabProfile, Pod, Device, ConsoleServer, ConsoleServerPort


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public')


class LabProfileAdmin(admin.ModelAdmin):
    list_display = ('lab', 'last_edited', 'last_edited_by')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pod', 'port')
    readonly_fields = ('slug',)


class PodAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab')
    readonly_fields = ('slug',)


class ConsoleServerPortInline(admin.TabularInline):
    model = ConsoleServerPort


class ConsoleServerPortAdmin(admin.ModelAdmin):
    list_display = ('consoleserver', 'number', 'device', 'telnet_port', 'ssh_port')


class ConsoleServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lab', 'fqdn', 'ip4_address')
    inlines = [
        ConsoleServerPortInline,
    ]


admin.site.register(Lab, LabAdmin)
admin.site.register(LabProfile, LabProfileAdmin)
admin.site.register(Pod, PodAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(ConsoleServerPort, ConsoleServerPortAdmin)
admin.site.register(ConsoleServer, ConsoleServerAdmin)
