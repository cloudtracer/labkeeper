from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from django_bleach.models import BleachField


class Lab(models.Model):
    name = models.CharField('Name', max_length=80, unique=True)
    is_public = models.BooleanField('Public', default=True)
    is_active = models.BooleanField('Active', default=False)

    class Meta:
        pass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lab', kwargs={'id': self.id})

    def get_members(self):
        return [m.user for m in self.memberships.all()]

    def get_admins(self):
        return [m.user for m in self.memberships.filter(role__in=(Membership.ADMIN, Membership.OWNER))]

    def get_owners(self):
        return [m.user for m in self.memberships.filter(role=Membership.OWNER)]


class LabProfile(models.Model):
    lab = models.OneToOneField(Lab, related_name='profile')
    last_edited = models.DateTimeField('Last edited', auto_now=True, editable=False)
    last_edited_by = models.ForeignKey(User, editable=False, null=True)
    content = BleachField(blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return "Profile for {0}".format(self.lab.name)


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


class ConsoleServer(models.Model):
    lab = models.ForeignKey(Lab, related_name='consoleservers')
    devices = models.ManyToManyField(Device, through='ConsoleServerPort')
    name = models.CharField('Name', max_length=30)
    fqdn = models.CharField('Domain name', max_length=50, unique=True, blank=True)
    ip4_address = models.GenericIPAddressField('IPv4 address', protocol='IPv4')
    secret = models.CharField('Shared secret', max_length=30, default='')

    class Meta:
        unique_together = (
            ('lab', 'name'),
            ('lab', 'fqdn'),
            ('lab', 'ip4_address'),
        )

    def __unicode__(self):
        return self.name


class ConsoleServerPort(models.Model):
    consoleserver = models.ForeignKey(ConsoleServer, related_name='ports')
    device = models.OneToOneField(Device, related_name='port')
    number = models.PositiveIntegerField('Port number')
    telnet_port = models.PositiveIntegerField('Telnet port', blank=True)
    ssh_port = models.PositiveIntegerField('SSH port', blank=True)

    class Meta:
        unique_together = (
            ('consoleserver', 'number'),
        )

    def __unicode__(self):
        return "{0} port {1}".format(self.consoleserver, self.number)


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

    class Meta:
        unique_together = (('user', 'lab'),)

    def __unicode__(self):
        return "{0} is a member of {1}".format(self.user, self.lab)
