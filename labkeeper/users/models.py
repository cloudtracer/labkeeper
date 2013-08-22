import pytz

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from django_countries import CountryField

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
)

TIMEZONE_CHOICES = [(tz, timezone.now().astimezone(pytz.timezone(tz)).strftime("[UTC%z] {0}".format(name)))
                    for tz, name in settings.SUPPORTED_TIMEZONES.items()]

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', editable=False)
    last_active = models.DateTimeField('Last active', blank=True, null=True, editable=False)
    birth_date = models.DateField('Birth date', blank=True, null=True)
    gender = models.PositiveSmallIntegerField('Gender', choices=GENDER_CHOICES, blank=True, null=True)
    country = CountryField(blank=True)
    timezone = models.CharField('Timezone', max_length=40, choices=TIMEZONE_CHOICES, default='UTC')
    location = models.CharField('Location', max_length=50, blank=True)
    twitter = models.CharField('Twitter', max_length=15, blank=True)
    facebook = models.CharField('Facebook', max_length=50, blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return "Profile for {0}".format(self.user.username)

    def get_absolute_url(self):
        return reverse('users_profile', kwargs={'username': self.user.username})

def create_profile_for_user(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_profile_for_user, sender=User)
