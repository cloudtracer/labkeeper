import pytz

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserProfileForm


def login(request):

    redirect_to = request.GET.get('next')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            # Log the user in and set his preferred timezone
            auth_login(request, form.get_user())
            request.session['django_timezone'] = pytz.timezone(form.get_user().profile.timezone)

            messages.success(request, "Welcome {0}! You are logged in.".format(request.user))
            if not redirect_to.strip() or '//' in redirect_to:
                return redirect(reverse('home'))
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()

    return render(request, 'users/login.html', {
        'form': form,
        'next': redirect_to,
        })


def logout(request):

    auth_logout(request)

    messages.info(request, "You have logged out.")
    return redirect(reverse('users_login'))


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
