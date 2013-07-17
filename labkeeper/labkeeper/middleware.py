from django.utils import timezone

# From https://docs.djangoproject.com/en/dev/topics/i18n/timezones/
class TimezoneMiddleware(object):
    def process_request(self, request):
        tz = request.session.get('django_timezone')
        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()
