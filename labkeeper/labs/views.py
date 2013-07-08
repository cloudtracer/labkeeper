from django.shortcuts import get_object_or_404, redirect, render

from labs.models import Lab
from labs.forms import LabProfileForm

def default(request):

    return render(request, 'labs/default.html', {
        'labs': Lab.objects.filter(is_public=True),
        })

def lab(request, id):

    lab = get_object_or_404(Lab, id=id)

    return render(request, 'labs/lab.html', {
        'lab': lab,
        })

def lab_edit(request, id):

    # TODO: Permission checking

    lab = get_object_or_404(Lab, id=id)

    # Processing a submitted form
    if request.method == 'POST':
        form = LabProfileForm(request.POST, instance=lab.profile)
        if form.is_valid():
            form.save()
            return redirect(lab.get_absolute_url())

    form = LabProfileForm(instance=lab.profile)

    return render(request, 'labs/lab_edit.html', {
        'lab': lab,
        'form': form,
        })
