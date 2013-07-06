from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from labs.models import Pod


class Reservation(models.Model):
    """A reservation made by a User for a Pod."""

    user = models.ForeignKey(User, related_name='reservations')
    pod = models.ForeignKey(Pod, related_name='reservations')
    created_time = models.DateTimeField('Time created', auto_now_add=True)
    created_ip_address = models.GenericIPAddressField('IP of creator', blank=True, null=True)
    start_time = models.DateTimeField('Start time')
    duration = models.PositiveSmallIntegerField('Duration (hours)')
    end_time = models.DateTimeField('End time', editable=False, null=True)
    password = models.CharField('Password', max_length=16)

    class Meta:
        pass

    def __unicode__(self):
        return "{0} reserved by {1} at {2}".format(self.pod, self.user, self.start_time)

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + timedelta(hours=self.duration)
        super(Reservation, self).save(*args, **kwargs)

    # Returns time left (timedelta)
    def _get_time_left(self):
        if self.start_time <= timezone.now() and self.end_time > timezone.now():
            return self.end_time - timezone.now()
        return None
    time_left = property(_get_time_left)
