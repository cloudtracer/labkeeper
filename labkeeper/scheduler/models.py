from django.contrib.auth.models import User
from django.db import models

from labs.models import Pod


class Reservation(models.Model):
    """A reservation made by a User for a Pod."""

    user = models.ForeignKey(User, related_name='reservations')
    pod = models.ManyToManyField(Pod, related_name='reservations')
    created_time = models.DateTimeField('Time created', auto_now_add=True)
    created_ip_address = models.GenericIPAddressField('IP of creator', blank=True)
    start_time = models.DateTimeField('Start time')
    duration = models.PositiveSmallIntegerField('Duration (hours)')
    password = models.CharField('Password', max_length=16)

    class Meta:
        pass

    def __unicode__(self):
        return "{0} reserved by {1} at {2}".format(self.pod, self.user, self.start_time)
