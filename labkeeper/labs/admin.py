from django.contrib import admin

from labs.models import *


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public', 'is_active')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pod', 'cs_port')
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


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'role')


class MembershipInvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'lab', 'sent')


admin.site.register(Lab, LabAdmin)
admin.site.register(Pod, PodAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(ConsoleServerPort, ConsoleServerPortAdmin)
admin.site.register(ConsoleServer, ConsoleServerAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(MembershipInvitation, MembershipInvitationAdmin)
