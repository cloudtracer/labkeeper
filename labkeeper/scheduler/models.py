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
        pass

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
    def _get_midnight_split(self):
        x = 24 - self.start_time.hour
        if x < self.duration:
            return (x, self.duration - x)
        else:
            return (self.duration, 0)
    midnight_split = property(_get_midnight_split)


class Schedule:

    def __init__(self, lab, start_day, days=7):

        self.start_day = start_day
        
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
            for d in rrule.rrule(rrule.DAILY, dtstart=datetime.combine(start_day, time(0, 0)), count=days):
                self.schedule[h][d.date().day] = {}
                for p, i in self.pod_index.items():
                    self.schedule[h][d.date().day][i] = None

        # Assign Reservations to schedule
        for r in Reservation.objects.filter(lab=lab):
            for p in r.pods.all():
                self.schedule[r.start_time.hour][r.start_time.day][self.pod_index[p.id]] = r
                if r.midnight_split:
                    self.schedule[0][r.start_time.day+1][self.pod_index[p.id]] = r

    def get_weekdays(self):
        return [(self.start_day + timedelta(days=i)).strftime("%b %d (%a)") for i in range(7)]