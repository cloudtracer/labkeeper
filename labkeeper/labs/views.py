from django.shortcuts import render, get_object_or_404

from labs.models import Lab

def default(request):

    return render(request, 'labs/default.html', {
        'labs': Lab.objects.filter(is_public=True),
        })

def lab(request, id):

    lab = get_object_or_404(Lab, id=id)

    return render(request, 'labs/lab.html', {
        'lab': lab,
        })
