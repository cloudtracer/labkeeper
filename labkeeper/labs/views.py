from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from labs.models import Device, Lab, Pod
from labs.forms import PodForm, LabProfileForm

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
    DeviceFormSet = modelformset_factory(Device, can_delete=True, extra=1)

    if request.method == 'POST':
        formset = DeviceFormSet(request.POST)
        for form in formset:
            form.fields['pod'].queryset = Pod.objects.filter(lab=lab)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('labs_manage_devices', kwargs={'id': lab.id}))
    else:
        formset = DeviceFormSet(queryset=Device.objects.filter(pod__lab=lab))
        for form in formset:
            form.fields['pod'].queryset = Pod.objects.filter(lab=lab)

    return render(request, 'labs/manage_devices.html', {
        'lab': lab,
        'formset': formset,
        'nav_labs_manage': 'devices',
        })

def manage_pods(request, id):

    # TODO: Permission checking

    lab = get_object_or_404(Lab, id=id)

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
        'nav_labs_manage': 'pods',
        })

def delete_pod(request, id):

    # TODO: Permission checking
    # TODO: Prevent deletion of Pods which still have one or more Devices assigned

    pod = get_object_or_404(Pod, id=id)
    pod.delete()

    return redirect(reverse('labs_manage_pods', kwargs={'id': pod.lab.id}))
