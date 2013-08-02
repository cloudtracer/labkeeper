import pytz
from datetime import datetime
from dateutil import parser

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from scheduler.models import Schedule

from labs.models import ConsoleServer, ConsoleServerPort, Device, Lab, Pod
from labs.forms import ConsoleServerForm, ConsoleServerPortForm, LabForm, NewConsoleServerForm, PodForm
from scheduler.models import Reservation
from scheduler.forms import ReservationForm


def default(request):

    return render(request, 'labs/default.html', {
        'lab_list': Lab.objects.filter(is_active=True),
        })


def lab(request, lab_id):

    lab = get_object_or_404(Lab.objects.prefetch_related('pods__devices'), id=lab_id)

    return render(request, 'labs/lab.html', {
        'lab': lab,
        'nav_labs': 'dashboard',
        })


def schedule(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)

    # Hack to set request's timezone
    request.session['django_timezone'] = pytz.timezone('US/Eastern')
    #request.session['django_timezone'] = pytz.timezone('Canada/Newfoundland')

    # Generate the Lab's schedule for the next seven days
    schedule = Schedule(lab, tz=request.session.get('django_timezone'))

    # Determine if the current User is allowed to make a Reservation
    if request.user in lab.admins:
        reservation_forbidden = False
    elif not lab.is_active:
        reservation_forbidden = "Sorry, this lab is not currently accepting new reservations."
    elif not lab.is_public and request.user not in lab.members:
        reservation_forbidden = "Sorry, only members can reserve time in this lab."
    elif lab.max_rsv_per_user and lab.reservations.filter(user=request.user, end_time__gt=timezone.now()).count() >= lab.max_rsv_per_user:
        reservation_forbidden = "Sorry, you have reached the maximum number of reservations for this lab ({0}).".format(lab.max_rsv_per_user)
    else:
        reservation_forbidden = False

    # Creating a new Reservation
    if not reservation_forbidden and request.method == 'POST':
        reservation_form = ReservationForm(lab, schedule, request.session['django_timezone'], request.POST)
        if reservation_form.is_valid():
            # Create a full datetime from the individual date and time fields, then make it timezone-aware
            start_time = parser.parse(' '.join((reservation_form.cleaned_data['date'], reservation_form.cleaned_data['time'])))
            start_time = request.session.get('django_timezone').localize(start_time)
            # Create the Reservation
            r = Reservation.objects.create(
                user = request.user,
                lab = lab,
                # TODO: Add awareness of X-FORWARDED-FOR header?
                created_ip_address = request.META.get('REMOTE_ADDR'),
                start_time = start_time,
                duration = int(reservation_form.cleaned_data['duration'])
            )
            # Add reserved Pod(s) to the Reservation
            if isinstance(reservation_form.cleaned_data['pods'], basestring):
                r.pods.add(lab.pods.get(id=reservation_form.cleaned_data['pods']))
            else:
                for pod_id in reservation_form.cleaned_data['pods']:
                    r.pods.add(lab.pods.get(id=pod_id))
            messages.success(request, "Your reservation has been created.")
            return redirect(reverse('scheduler_reservation', kwargs={'rsv_id': r.id}))
    elif not reservation_forbidden:
        reservation_form = ReservationForm(lab, schedule, request.session['django_timezone'])
    else:
        reservation_form = None

    return render(request, 'labs/schedule.html', {
        'lab': lab,
        'lab_open_hours': [h.hour for h in lab.get_open_hours(tz=request.session.get('django_timezone'))],
        'reservation_forbidden': reservation_forbidden,
        'reservation_form': reservation_form,
        's': schedule,
        'current_time': datetime.now(),
        'nav_labs': 'schedule',
        })


def member_list(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)

    return render(request, 'labs/member_list.html', {
        'lab': lab,
        'member_list': lab.memberships.all(),
        'nav_labs': 'members',
        })


def edit_lab(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)
    if request.user not in lab.owners:
        return HttpResponseForbidden()

    # Processing a submitted form
    if request.method == 'POST':
        form = LabForm(request.POST, instance=lab)
        if form.is_valid():
            p = form.save()
            p.last_edited_by = request.user
            p.save()
            messages.success(request, "Your changes have been saved.")
            return redirect(reverse('labs_edit_lab', kwargs={'lab_id': lab.id}))
    else:
        form = LabForm(instance=lab)

    return render(request, 'labs/edit_lab.html', {
        'lab': lab,
        'form': form,
        'nav_labs': 'manage',
        'nav_labs_manage': 'profile',
        })


def manage_pods(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)
    if request.user not in lab.owners:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PodForm(request.POST)
        if form.is_valid():
            new_pod = form.save(commit=False)
            new_pod.lab = lab
            new_pod.save()
            form = PodForm()
    else:
        form = PodForm()

    return render(request, 'labs/manage_pods.html', {
        'lab': lab,
        'pod_list': lab.pods.all(),
        'form': form,
        'nav_labs': 'manage',
        'nav_labs_manage': 'pods',
        })


def edit_pod(request, pod_id):

    pod = get_object_or_404(Pod, id=pod_id)
    if request.user not in pod.lab.owners:
        return HttpResponseForbidden()

    if request.method == 'POST':
        pod_form = PodForm(request.POST, instance=pod)
        if pod_form.is_valid():
            pod_form.save()
            messages.success(request, "Your changes have been saved.")
    else:
        pod_form = PodForm(instance=pod)

    return render(request, 'labs/edit_pod.html', {
        'lab': pod.lab,
        'pod': pod,
        'pod_form': pod_form,
        'nav_labs': 'manage',
        'nav_labs_manage': 'pods',
        })


def delete_pod(request, pod_id):

    pod = get_object_or_404(Pod, id=pod_id)
    if request.user not in pod.lab.owners:
        return HttpResponseForbidden()

    # Don't delete a Pod which has one or more Devices assigned
    if pod.devices.all():
        messages.error(request, "Cannot delete a pod which has devices assigned.")
    else:
        pod.delete()
        messages.success(request, "Pod {0} has been deleted.".format(pod.name))

    return redirect(reverse('labs_manage_pods', kwargs={'lab_id': pod.lab.id}))


def manage_consoleservers(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)
    if request.user not in lab.owners:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = NewConsoleServerForm(request.POST)
        if form.is_valid():
            # Create the new ConsoleServer
            new_consoleserver = form.save(commit=False)
            new_consoleserver.lab = lab
            new_consoleserver.save()
            messages.success(request, "Created console server {0}".format(new_consoleserver.name))
            # If directed, create n initial ConsoleServerPorts
            if form.cleaned_data['port_count']:
                for i in range(int(form.cleaned_data['port_count'])):
                    ConsoleServerPort.objects.create(
                        consoleserver = new_consoleserver,
                        number = form.cleaned_data['base_port_number'] + i,
                        telnet_port = form.cleaned_data['base_telnet_port'] + i,
                        ssh_port = form.cleaned_data['base_ssh_port'] + i
                    )
                messages.success(request, "Created {0} console server ports".format(i + 1))
            return redirect(reverse('labs_edit_consoleserver', kwargs={'cs_id': new_consoleserver.id}))
    else:
        form = NewConsoleServerForm()

    return render(request, 'labs/manage_consoleservers.html', {
        'lab': lab,
        'cs_list': lab.consoleservers.annotate(port_count=Count('ports')),
        'form': form,
        'nav_labs': 'manage',
        'nav_labs_manage': 'consoleservers',
        })


def edit_consoleserver(request, cs_id):

    cs = get_object_or_404(ConsoleServer, id=cs_id)
    if request.user not in cs.lab.owners:
        return HttpResponseForbidden()

    ConsoleServerPortFormSet = inlineformset_factory(ConsoleServer, ConsoleServerPort, form=ConsoleServerPortForm, extra=4, max_num=48)

    # Editing the ConsoleServer
    if request.POST.get('form') == 'consoleserver':
        cs_form = ConsoleServerForm(request.POST, instance=cs)
        if cs_form.is_valid():
            cs_form.save()
            messages.success(request, "Your changes have been saved.")
    else:
        cs_form = ConsoleServerForm(instance=cs)

    # Bulk-editing the ConsoleServerPorts
    if request.POST.get('form') == 'ports':
        port_formset = ConsoleServerPortFormSet(request.POST, instance=cs)
        if port_formset.is_valid():
            port_formset.save()
            port_formset = ConsoleServerPortFormSet(instance=cs)
    else:
        port_formset = ConsoleServerPortFormSet(instance=cs)

    return render(request, 'labs/edit_consoleserver.html', {
        'lab': cs.lab,
        'cs': cs,
        'cs_form': cs_form,
        'port_formset': port_formset,
        'nav_labs': 'manage',
        'nav_labs_manage': 'consoleservers',
        })


def delete_consoleserver(request, cs_id):

    cs = get_object_or_404(ConsoleServer, id=cs_id)
    if request.user not in cs.lab.owners:
        return HttpResponseForbidden()

    # Don't delete a ConsoleServer with one or more Devices assigned
    if Device.objects.filter(cs_port__consoleserver=cs):
        messages.error(request, "Cannot delete a console server which has devices assigned.")
    else:
        cs.delete()
        messages.success(request, "Console server {0} has been deleted.".format(cs.name))

    return redirect(reverse('labs_manage_consoleservers', kwargs={'lab_id': cs.lab.id}))


def manage_devices(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)
    if request.user not in lab.owners:
        return HttpResponseForbidden()

    # TODO: This formset generates excessive SQL queries; any way to optimize it?
    DeviceFormSet = modelformset_factory(Device, can_delete=True, extra=3)
    if request.method == 'POST':
        formset = DeviceFormSet(request.POST, queryset=Device.objects.filter(pod__lab=lab))
        for form in formset:
            form.fields['pod'].choices = Pod.objects.filter(lab=lab)
            form.fields['cs_port'].queryset = ConsoleServerPort.objects.filter(consoleserver__lab=lab)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('labs_manage_devices', kwargs={'lab_id': lab.id}))
    else:
        formset = DeviceFormSet(queryset=Device.objects.filter(pod__lab=lab))
        for form in formset:
            form.fields['pod'].queryset = Pod.objects.filter(lab=lab)
            form.fields['cs_port'].queryset = ConsoleServerPort.objects.filter(consoleserver__lab=lab)

    return render(request, 'labs/manage_devices.html', {
        'lab': lab,
        'formset': formset,
        'nav_labs': 'manage',
        'nav_labs_manage': 'devices',
        })
