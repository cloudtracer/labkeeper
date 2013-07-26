import pytz
from datetime import datetime, time, timedelta
from dateutil import rrule

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from labs.models import Lab, Pod


class Reservation(models.Model):
    """A reservation made by a User for a Pod."""

    user = models.ForeignKey(User, related_name='reservations')
    lab = models.ForeignKey(Lab, related_name='reservations')
    pods = models.ManyToManyField(Pod, related_name='reservations')
    created_time = models.DateTimeField('Time created', auto_now_add=True)
    created_ip_address = models.GenericIPAddressField('IP of creator', blank=True, null=True)
    start_time = models.DateTimeField('Start time')
    duration = models.PositiveSmallIntegerField('Duration (hours)')
    end_time = models.DateTimeField('End time', editable=False, null=True)
    password = models.CharField('Password', max_length=16)

    class Meta:
        unique_together = (
            ('user', 'password'),
        )

    def __unicode__(self):
        return "{0} reserved by {1} at {2}".format(self.get_pods(), self.user, self.start_time)

    def get_absolute_url(self):
        return reverse('reservation', kwargs={'rsv_id': self.id})

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + timedelta(hours=self.duration)
        super(Reservation, self).save(*args, **kwargs)

    # For admin list_display
    def get_pods(self):
        return ', '.join([p.name for p in self.pods.all()])
    get_pods.short_description = 'Pods'

    # Returns time left (timedelta)
    def _get_time_left(self):
        if self.start_time <= timezone.now() and self.end_time > timezone.now():
            return self.end_time - timezone.now()
        return None
    time_left = property(_get_time_left)

    # Split total duration into hours (before, after) midnight
    # for schedule presentation
    def get_midnight_split(self, timezone):
        start_time = self.start_time.astimezone(tz=timezone)
        mins_before_midnight = (24 - start_time.hour)*60 - start_time.minute
        if mins_before_midnight < self.duration*60:
            return (mins_before_midnight, self.duration*60 - mins_before_midnight)
        else:
            return None


class ScheduleBlock:

    def __init__(self, duration, url, offset=0, wrap=False, unwrap=False):
        self.duration = duration
        self.url = url
        self.offset = offset
        self.wrap = wrap
        self.unwrap = unwrap


class Schedule:

    def __init__(self, lab, tz=None, days=7):

        self.tz = tz or pytz.timezone('UTC')

        # Initialize schedule's starting and ending timezone-aware datetimes
        self.start_day = timezone.now().astimezone(self.tz).date()
        self.end_day = self.start_day + timedelta(days)

        # Compile index of Pods for this Lab
        self.pod_index = {}
        i = 1
        for pod in lab.pods.all():
            self.pod_index[pod.id] = i
            i += 1

        # Build the schedule skeleton of 24 hours * 7 days * n Pods
        self.schedule = {}
        for h in range(24):
            self.schedule[h] = {}
            for d in rrule.rrule(rrule.DAILY, dtstart=datetime.combine(self.start_day, time()), count=days):
                self.schedule[h][d.date().day] = {}
                for p, i in self.pod_index.items():
                    self.schedule[h][d.date().day][i] = None

        # Assign Reservations to schedule
        for r in lab.reservations.filter(
                    models.Q(start_time__range=(self.start_day, self.end_day)) |
                    models.Q(end_time__range=(self.start_day, self.end_day))
                ).select_related('pods'):
            for p in r.pods.all():
                # Convert Reservation start and end times to the current timezone
                start_time = r.start_time.astimezone(tz=self.tz)
                end_time = r.end_time.astimezone(tz=self.tz)
                midnight_split = r.get_midnight_split(self.tz)
                if midnight_split:
                    # Create two ScheduleBocks (one for each day) and wrap them
                    if start_time.date() >= self.start_day:
                        self.schedule[start_time.hour][start_time.day][self.pod_index[p.id]] = ScheduleBlock(midnight_split[0], r.get_absolute_url(), offset=start_time.minute, wrap=True)
                    if end_time.date() < self.end_day:
                        self.schedule[0][start_time.day+1][self.pod_index[p.id]] = ScheduleBlock(midnight_split[1], r.get_absolute_url(), unwrap=True)
                else:
                    self.schedule[start_time.hour][start_time.day][self.pod_index[p.id]] = ScheduleBlock(r.duration*60, r.get_absolute_url())

    def get_weekdays(self):
        return [(self.start_day + timedelta(days=i)).strftime("%b %d (%a)") for i in range(7)]
