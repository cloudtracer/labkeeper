import pytz

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserProfileForm


def profile(request, username):

    user = get_object_or_404(User, username=username)

    return render(request, 'users/profile.html', {
        'profile': user.profile,
        })


def edit_profile(request, username):

    user = get_object_or_404(User, username=username)
    if request.user != user:
        return HttpResponseForbidden()

    # Processing a submitted form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            request.session['django_timezone'] = pytz.timezone(form.cleaned_data['timezone'])
            messages.success(request, "Your profile has been updated.")
            return redirect(reverse('users_profile', kwargs={'username': user.username}))
    else:
        form = UserProfileForm(instance=user.profile)

    return render(request, 'users/edit_profile.html', {
        'profile': user.profile,
        'form': form,
        })
