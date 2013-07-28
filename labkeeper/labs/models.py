import pytz

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from django_bleach.models import BleachField

class Lab(models.Model):
    HOURS = [(i, "{0}:00".format(i)) for i in range(24)]

    name = models.CharField('Name', max_length=80, unique=True)
    is_public = models.BooleanField('Public', default=True, help_text="This lab is viewable by everyone")
    is_active = models.BooleanField('Active', default=False, help_text="This lab is open for new reservations")
    opening_time = models.PositiveSmallIntegerField('Opens at', choices=HOURS, blank=True, null=True, help_text="UTC time")
    closing_time = models.PositiveSmallIntegerField('Closes at', choices=HOURS, blank=True, null=True, help_text="UTC time")
    allow_multipod = models.BooleanField('Multi-pod reservations', default=True, help_text="Allow users to reserve multiple pods at once")
    min_reservation = models.PositiveSmallIntegerField('Minimum reservation', choices=[(i, i) for i in range(1, 13)], default=2,
                                                       help_text="Minimum reservation time (in hours)")
    max_reservation = models.PositiveSmallIntegerField('Maximum reservation', choices=[(i, i) for i in range(1, 13)], default=6,
                                                       help_text="Maximum reservation time (in hours)")
    profile = BleachField(blank=True)
    last_edited = models.DateTimeField('Last edited', auto_now=True, editable=False)
    last_edited_by = models.ForeignKey(User, editable=False, null=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lab', kwargs={'lab_id': self.id})

    def get_members(self):
        return [m.user for m in self.memberships.all()]

    def get_admins(self):
        return [m.user for m in self.memberships.filter(role__in=(Membership.ADMIN, Membership.OWNER))]

    def get_owners(self):
        return [m.user for m in self.memberships.filter(role=Membership.OWNER)]

    def _get_open_hours(self):
        """Return a list of hours during which the Lab is available each day"""
        if self.opening_time and not self.closing_time:
            return range(self.opening_time, 24)
        if not self.opening_time and self.closing_time:
            return range(0, self.closing_time)
        if self.opening_time < self.closing_time:
            return range(self.opening_time, self.closing_time)
        if self.opening_time > self.closing_time:
            return range(self.opening_time, 24) + range(0, self.closing_time)
        return range(0, 24)
    open_hours = property(_get_open_hours)


class Pod(models.Model):
    lab = models.ForeignKey(Lab, related_name='pods')
    name = models.CharField('Name', max_length=30, default='')
    slug = models.SlugField('Slug', max_length=30, editable=False)

    class Meta:
        ordering = ['name']
        unique_together = (
            ('lab', 'name'),
        )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pod, self).save(*args, **kwargs)


class ConsoleServer(models.Model):
    lab = models.ForeignKey(Lab, related_name='consoleservers')
    name = models.CharField('Name', max_length=30)
    fqdn = models.CharField('Domain name', max_length=50, unique=True, blank=True, null=True)
    ip4_address = models.GenericIPAddressField('IPv4 address', protocol='IPv4', unique=True, blank=True, null=True)
    secret = models.CharField('Shared secret', max_length=30, default='')

    class Meta:
        unique_together = (
            ('lab', 'ip4_address'),
        )

    def __unicode__(self):
        return self.name


class ConsoleServerPort(models.Model):
    consoleserver = models.ForeignKey(ConsoleServer, related_name='ports')
    number = models.PositiveIntegerField('Port number')
    telnet_port = models.PositiveIntegerField('Telnet port', blank=True, null=True)
    ssh_port = models.PositiveIntegerField('SSH port', blank=True, null=True)

    class Meta:
        unique_together = (
            ('consoleserver', 'number'),
            ('consoleserver', 'telnet_port'),
            ('consoleserver', 'ssh_port'),
        )

    def __unicode__(self):
        return "{0} - Port {1}".format(self.consoleserver, self.number)


class Device(models.Model):
    ROUTER = 0
    L2_SWITCH = 1
    L3_SWITCH = 2
    FIREWALL = 3
    OTHER = 255
    DEVICE_TYPES = (
        (ROUTER, 'Router'),
        (L2_SWITCH, 'Layer 2 Switch'),
        (L3_SWITCH, 'Layer 3 Switch'),
        (FIREWALL, 'Firewall'),
        (OTHER, 'Other'),
    )

    pod = models.ForeignKey(Pod, related_name='devices')
    cs_port = models.OneToOneField(ConsoleServerPort, related_name='device', unique=True)
    name = models.CharField('Name', max_length=30)
    slug = models.SlugField('Slug', max_length=30, editable=False)
    type = models.PositiveSmallIntegerField('Type', choices=DEVICE_TYPES, default=ROUTER)
    description = models.CharField('Description', max_length=80, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = (
            ('pod', 'name'),
            ('pod', 'slug'),
        )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Device, self).save(*args, **kwargs)


class Membership(models.Model):
    MEMBER = 0
    ADMIN = 1
    OWNER = 2
    MEMBERSHIP_ROLES = (
        (MEMBER, 'Member'),
        (ADMIN, 'Admin'),
        (OWNER, 'Owner'),
    )

    user = models.ForeignKey(User, related_name='memberships')
    lab = models.ForeignKey(Lab, related_name='memberships')
    role = models.PositiveSmallIntegerField('Role', choices=MEMBERSHIP_ROLES, default=MEMBER)
    joined = models.DateField('Joined', auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'lab'),
        )

    def __unicode__(self):
        return "{0} is a(n) {1} of {2}".format(self.user, self.get_role_display(), self.lab)
