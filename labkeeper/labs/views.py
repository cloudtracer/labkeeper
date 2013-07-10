from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from labs.models import Device, Lab, Pod
from labs.forms import LabProfileForm

def default(request):

    return render(request, 'labs/default.html', {
        'lab_list': Lab.objects.filter(is_public=True),
        })

def lab(request, id):

    lab = get_object_or_404(Lab, id=id)

    return render(request, 'labs/lab.html', {
        'lab': lab,
        })

def manage_profile(request, id):

    # TODO: Permission checking

    lab = get_object_or_404(Lab, id=id)

    # Processing a submitted form
    if request.method == 'POST':
        form = LabProfileForm(request.POST, instance=lab.profile)
        if form.is_valid():
            p = form.save()
            p.last_edited_by = request.user
            p.save()
            return redirect(lab.get_absolute_url())
    else:
        form = LabProfileForm(instance=lab.profile)

    return render(request, 'labs/manage_profile.html', {
        'lab': lab,
        'form': form,
        'nav_labs_manage': 'profile',
        })

def manage_devices(request, id):

    # TODO: Permission checking

    lab = get_object_or_404(Lab, id=id)
    DeviceFormSet = modelformset_factory(Device, extra=1)

    # Processing a submitted formset
    if request.method == 'POST':
        formset = DeviceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('labs_manage_devices', kwargs={'id': lab.id}))
    else:
        formset = DeviceFormSet(queryset=Device.objects.filter(pod__lab=lab))

    return render(request, 'labs/manage_devices.html', {
        'lab': lab,
        'formset': formset,
        'nav_labs_manage': 'devices',
        })

def manage_pods(request, id):

    # TODO: Permission checking

    lab = get_object_or_404(Lab, id=id)
    PodFormSet = modelformset_factory(Pod, fields=['name'], extra=1)

    # Processing a submitted formset
    if request.method == 'POST':
        formset = PodFormSet(request.POST)
        if formset.is_valid():
            for podform in formset.save(commit=False):
                podform.lab = lab
                podform.save()
            return redirect(reverse('labs_manage_pods', kwargs={'id': lab.id}))
    else:
        formset = PodFormSet(queryset=Pod.objects.filter(lab=lab))

    return render(request, 'labs/manage_pods.html', {
        'lab': lab,
        'formset': formset,
        'nav_labs_manage': 'pods',
        })
