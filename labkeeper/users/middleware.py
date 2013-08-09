from django.utils import timezone

from users.models import UserProfile


class UserTracking:
    """
    Update last_active times of authenticated Users.
    """

    def process_request(self, request):

        # Ignore AJAX requests
        if request.user.is_authenticated() and not request.is_ajax():
            UserProfile.objects.filter(user=request.user).update(last_active=timezone.now())
