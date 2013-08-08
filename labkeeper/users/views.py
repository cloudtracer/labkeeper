from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.models import User


def profile(request, username):

    user = get_object_or_404(User, username=username)

    return render(request, 'users/profile.html', {
        'profile': user.profile,
        })