from django.contrib import admin

from scheduler.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'pod', 'created_time', 'start_time', 'duration')


admin.site.register(Reservation, ReservationAdmin)
