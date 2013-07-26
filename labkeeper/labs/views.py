import pytz
from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from scheduler.models import Schedule

from labs.models import ConsoleServer, ConsoleServerPort, Device, Lab, Pod
from labs.forms import ConsoleServerForm, ConsoleServerPortForm, LabForm, PodForm
from scheduler.forms import ReservationForm


def default(request):

    return render(request, 'labs/default.html', {
        'lab_list': Lab.objects.filter(is_public=True),
        })


def lab(request, lab_id):

    lab = get_object_or_404(Lab.objects.prefetch_related('pods__devices'), id=lab_id)

    return render(request, 'labs/lab.html', {
        'lab': lab,
        'nav_labs': 'dashboard',
        })


def schedule(request, lab_id):

    lab = get_object_or_404(Lab, id=lab_id)

    request.session['django_timezone'] = pytz.timezone('Canada/Newfoundland')

    # Generate the Lab's schedule for the next seven days
    s = Schedule(lab, tz=request.session.get('django_timezone'))

    return render(request, 'labs/schedule.html', {
        'lab': lab,
        'reservation_form': ReservationForm(lab),
        's': s,
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
    if request.user not in lab.get_owners():
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
    if request.user not in lab.get_owners():
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
    if request.user not in pod.lab.get_owners():
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
    if request.user not in pod.lab.get_owners():
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
    if request.user not in lab.get_owners():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ConsoleServerForm(request.POST)
        if form.is_valid():
            new_consoleserver = form.save(commit=False)
            new_consoleserver.lab = lab
            new_consoleserver.save()
            form = ConsoleServerForm()
    else:
        form = ConsoleServerForm()

    return render(request, 'labs/manage_consoleservers.html', {
        'lab': lab,
        'cs_list': lab.consoleservers.annotate(port_count=Count('ports')),
        'form': form,
        'nav_labs': 'manage',
        'nav_labs_manage': 'consoleservers',
        })


def edit_consoleserver(request, cs_id):

    cs = get_object_or_404(ConsoleServer, id=cs_id)
    if request.user not in cs.lab.get_owners():
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
    if request.user not in cs.lab.get_owners():
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
    if request.user not in lab.get_owners():
        return HttpResponseForbidden()

    DeviceFormSet = modelformset_factory(Device, can_delete=True, extra=3)

    if request.method == 'POST':
        formset = DeviceFormSet(request.POST, queryset=Device.objects.filter(pod__lab=lab))
        for form in formset:
            form.fields['pod'].queryset = Pod.objects.filter(lab=lab)
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
