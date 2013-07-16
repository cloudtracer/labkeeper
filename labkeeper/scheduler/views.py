from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from scheduler.models import Reservation


def reservation(request, rsv_id):

    rsv = get_object_or_404(Reservation, id=rsv_id)

    return render(request, 'scheduler/reservation.html', {
        'rsv': rsv,
        })


def delete_reservation(request, rsv_id):

    rsv = get_object_or_404(Reservation, id=rsv_id)
    if request.user not in rsv.pod.lab.get_admins():
        return HttpResponseForbidden()

    rsv.delete()
    messages.info(request, "Your reservation has been deleted.")

    return redirect(reverse('my_reservations'))


def reservation_list(request, username=None):

    if username:
        user = get_object_or_404(User, username=username)
        rsv_list = user.reservations.all()
    else:
        rsv_list = request.user.reservations.all()

    return render(request, 'scheduler/reservation_list.html', {
        'rsv_list': rsv_list,
        })
