from django.contrib.auth.models import User
from django.db import models


class Lab(models.Model):
    name = models.CharField('Name', max_length=80, unique=True)
    is_public = models.BooleanField('Public', default=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.name


class Pod(models.Model):
    lab = models.ForeignKey(Lab, related_name='pods')
    name = models.CharField('Name', max_length=80, default='Default')

    class Meta:
        unique_together = (('lab', 'name'),)

    def __unicode__(self):
        return "Lab '{0}' - Pod '{1}'".format(self.lab, self.name)


class Device(models.Model):
    pod = models.ForeignKey(Pod, related_name='devices')
    name = models.CharField('Name', max_length=30)

    class Meta:
        unique_together = (('pod', 'name'),)

    def __unicode__(self):
        return self.name


class ConsoleServer(models.Model):
    lab = models.ForeignKey(Lab, related_name='consoleservers')
    devices = models.ManyToManyField(Device, through='ConsoleServerPort')
    name = models.CharField('Name', max_length=30)
    fqdn = models.CharField('Domain name', max_length=50, blank=True)
    ip4_address = models.GenericIPAddressField('IPv4 address', protocol='IPv4')
    secret = models.CharField('Shared secret', max_length=30, default='')

    class Meta:
        unique_together = (('lab', 'name'), ('lab', 'fqdn'), ('lab', 'ip4_address'))

    def __unicode__(self):
        return self.name


class ConsoleServerPort(models.Model):
    consoleserver = models.ForeignKey(ConsoleServer, related_name='ports')
    device = models.OneToOneField(Device, related_name='port')
    number = models.PositiveIntegerField('Port number')
    telnet_port = models.PositiveIntegerField('Telnet port', blank=True)
    ssh_port = models.PositiveIntegerField('SSH port', blank=True)

    class Meta:
        unique_together = (('consoleserver', 'number'),)

    def __unicode__(self):
        return "{0} port {1}".format(self.consoleserver, self.number)


class Membership(models.Model):
    user = models.ForeignKey(User, related_name='memberships')
    lab = models.ForeignKey(Lab, related_name='memberships')
    role = models.PositiveSmallIntegerField('Role')

    class Meta:
        unique_together = (('user', 'lab'),)

    def __unicode__(self):
        return "{0} is a member of {1}".format(self.user, self.lab)