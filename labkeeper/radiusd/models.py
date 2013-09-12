from django.contrib.auth.models import User
from django.db import models

from labs.models import Device, Lab


class RadiusLogin(models.Model):
    time = models.DateTimeField('Time', auto_now_add=True)
    lab = models.ForeignKey(Lab, related_name='radius_logins')
    device = models.ForeignKey(Device, related_name='radius_logins')
    user = models.ForeignKey(User, related_name='radius_logins')
    user_ip = models.GenericIPAddressField('User IP', blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return "{0} logged into {1} at {2}".format(self.user, self.device, self.time)
