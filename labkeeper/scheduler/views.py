from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from scheduler.models import Reservation
from scheduler.tables import ReservationTable


def reservation(request, rsv_id):

    rsv = get_object_or_404(Reservation.objects.select_related(), id=rsv_id)

    return render(request, 'scheduler/reservation.html', {
        'rsv': rsv,
        })


def delete_reservation(request, rsv_id):

    rsv = get_object_or_404(Reservation, id=rsv_id)
    if request.user != rsv.user and request.user not in rsv.lab.get_admins():
        return HttpResponseForbidden()

    rsv.delete()
    messages.info(request, "Your reservation has been deleted.")

    return redirect(reverse('scheduler_reservation_list'))


def reservation_list(request, username=None):

    if username:
        user = get_object_or_404(User, username=username)
        rsv_list = user.reservations.upcoming()
    else:
        rsv_list = request.user.reservations.upcoming()

    table = ReservationTable(rsv_list)

    return render(request, 'scheduler/reservation_list.html', {
        'username': username,
        'table': table,
        })
