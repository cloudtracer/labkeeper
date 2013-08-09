import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        if not request.session.get('django_timezone'):
            request.session['django_timezone'] = pytz.UTC
        timezone.activate(request.session.get('django_timezone'))
