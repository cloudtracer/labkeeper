from django.contrib import admin

from scheduler.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'duration', 'user', 'lab', 'get_pods', 'created_time')


admin.site.register(Reservation, ReservationAdmin)
