from datetime import date, datetime, time
import os
import pytz

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from django_bleach.models import BleachField
from django_countries import CountryField
from sorl.thumbnail import ImageField

class Lab(models.Model):
    """
    Represents an autonomous lab made up of up to four Pods and one or more ConsoleServers.

    Booleans:
    * is_public - Private Labs can only be reserved by members.
    * is_active - Inactive Labs do not show in the public Labs list and cannot be reserved by non-admins.
    * allow_multipod - A User can reserve multiple Pods simultaneously.
    """

    def _photo_filename(lab, filename):
        """Generate filename for uploaded Lab photo"""
        return "labs/photos/{0}{1}".format(lab.id, os.path.splitext(filename)[1])

    HOURS = [(i, "{0}:00".format(i)) for i in range(24)]

    name = models.CharField('Name', max_length=80, unique=True)
    country = CountryField()
    location = models.CharField('Location', max_length=80, blank=True, help_text="City, state, and/or region where the lab is physically located")
    founded = models.DateField('Founded', auto_now_add=True, editable=False)
    is_public = models.BooleanField('Public', default=True, help_text="Reservation is open to non-members")
    is_active = models.BooleanField('Active', default=False, help_text="This lab is open for new reservations")
    allow_multipod = models.BooleanField('Multi-pod reservations', default=True, help_text="Allow a user to reserve multiple pods at once")
    max_rsv_per_user = models.PositiveSmallIntegerField('Max reservations per user', default=1, help_text="The maximum number of active reservations an individual may have (0=disable)")
    opening_time = models.PositiveSmallIntegerField('Opens at', choices=HOURS, blank=True, null=True, help_text="UTC time")
    closing_time = models.PositiveSmallIntegerField('Closes at', choices=HOURS, blank=True, null=True, help_text="UTC time")
    min_reservation = models.PositiveSmallIntegerField('Minimum reservation time', choices=[(i, "%d hours" % i) for i in range(1, 13)], default=2,
                                                       help_text="Minimum reservation time")
    max_reservation = models.PositiveSmallIntegerField('Maximum reservation time', choices=[(i, "%d hours" % i) for i in range(1, 13)], default=6,
                                                       help_text="Maximum reservation time")
    photo = ImageField(upload_to=_photo_filename, blank=True)
    profile = BleachField(blank=True)
    last_edited = models.DateTimeField('Last edited', auto_now=True, editable=False)
    last_edited_by = models.ForeignKey(User, editable=False, null=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('labs_lab', kwargs={'lab_id': self.id})

    def _get_members(self):
        return [m.user for m in self.memberships.all()]
    members = property(_get_members)

    def _get_admins(self):
        return [m.user for m in self.memberships.filter(role__in=(Membership.ADMIN, Membership.OWNER))]
    admins = property(_get_admins)

    def _get_owners(self):
        return [m.user for m in self.memberships.filter(role=Membership.OWNER)]
    owners = property(_get_owners)

    def _get_map_address(self):
        if self.location:
            return "{0}, {1}".format(self.location, unicode(self.country))
        return unicode(self.country.name)
    map_address = property(_get_map_address)

    # Return a list of tz-aware hours during which the Lab is available each day
    def get_open_hours(self, tz=pytz.UTC):
        def make_hours(rng=range(0, 24)):
            return [datetime.combine(date.today(), time(h, tzinfo=pytz.UTC)).astimezone(tz).time() for h in rng]
        if self.opening_time and not self.closing_time:
            return make_hours(range(self.opening_time, 24))
        if not self.opening_time and self.closing_time:
            return make_hours(range(0, self.closing_time))
        if self.opening_time < self.closing_time:
            return make_hours(range(self.opening_time, self.closing_time))
        if self.opening_time > self.closing_time:
            return make_hours(range(self.opening_time, 24) + range(0, self.closing_time))
        return make_hours()


class Topology(models.Model):
    """
    An individual topology diagram for a Lab.
    """
    def _image_filename(topology, filename):
        """Generate filename for uploaded image"""
        return "labs/{0}/topologies/{1}".format(topology.lab.id, filename)

    lab = models.ForeignKey(Lab, related_name='topologies', editable=False)
    author = models.ForeignKey(User, related_name='topologies', editable=False)
    created = models.DateTimeField('Last edited', auto_now=True, editable=False)
    title = models.CharField('Name', max_length=80)
    image = ImageField(upload_to=_image_filename)

    class Meta:
        ordering = ['title']
        unique_together = (
            ('lab', 'image'),
        )
        verbose_name_plural = 'topologies'

    def __unicode__(self):
        return "Topology for {0}: {1}".format(self.lab, self.image.name)


class Pod(models.Model):
    """
    Pods are used to group Devices which belong to a common Lab and can be reserved individually.
    """

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
    """
    A console server is the "brain" of the lab through which users access devices. A ConsoleServer may have one or more
    ConsoleServerPorts to which Devices are attached.
    """

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
    """
    Represents a single physical port on a ConsoleServer. One Device may be attached per ConsoleServerPort.
    """

    consoleserver = models.ForeignKey(ConsoleServer, related_name='ports')
    number = models.PositiveIntegerField('Port ID')
    telnet_port = models.PositiveIntegerField('Telnet port', blank=True, null=True)
    ssh_port = models.PositiveIntegerField('SSH port', blank=True, null=True)

    class Meta:
        ordering = ['consoleserver', 'number']
        unique_together = (
            ('consoleserver', 'number'),
            ('consoleserver', 'telnet_port'),
            ('consoleserver', 'ssh_port'),
        )

    def __unicode__(self):
        return "Port {0}".format(self.number)


class Device(models.Model):
    """
    A device in a Lab which a User may access.
    """

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
    cs_port = models.OneToOneField(ConsoleServerPort, verbose_name='Console server port', related_name='device', unique=True)
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
    """
    The relation of a User to a Lab. A User can be a Lab member, admin, or owner.

    * Member - May reserve non-public Labs; not otherwise significant.
    * Admin - A member who may modify other members' reservations.
    * Owner - An admin who may manage Lab settings and components.
    """

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


class MembershipInvitation(models.Model):
    """
    An invitation from an owner or admin of a private lab to a non-member.
    """
    sender = models.ForeignKey(User, editable=False)
    recipient = models.ForeignKey(User, related_name='membership_invitations')
    lab = models.ForeignKey(Lab, related_name='membership_invitations', editable=False)
    sent = models.DateTimeField('Time sent', auto_now_add=True, editable=False)

    class Meta:
        unique_together = (
            ('recipient', 'lab'),
        )

    def __unicode__(self):
        return "{0} invited {1} to {2}".format(self.sender, self.recipient, self.lab)

    def accept(self):
        """User has accepted the invitation"""
        Membership.objects.create(user = self.recipient, lab = self.lab)
        self.delete()
