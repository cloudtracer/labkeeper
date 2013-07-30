from django.contrib import admin

from scheduler.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'duration', 'user', 'lab', 'pods_list', 'created_time')

    def pods_list(self, obj):
        return ', '.join(obj.get_pods())
    pods_list.short_description = 'Pods'


admin.site.register(Reservation, ReservationAdmin)
