from django.contrib.auth.models import User
from django.db import models


class Lab(models.Model):
    name = models.CharField('Name', max_length=80)
    is_public = models.BooleanField('Public', default=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.name


class Pod(models.Model):
    lab = models.ForeignKey(Lab, related_name='pods')
    name = models.CharField('Name', max_length=80, default='Default')

    class Meta:
        pass

    def __unicode__(self):
        return "Lab '{0}' - Pod '{1}'".format(self.lab, self.name)


class ConsoleServer(models.Model):
    lab = models.ForeignKey(Lab, related_name='consoleservers')
    name = models.CharField('Name', max_length=30)
    fqdn = models.CharField('Domain name', max_length=50, blank=True)
    ip4_address = models.GenericIPAddressField('IPv4 address', protocol='IPv4')
    secret = models.CharField('Shared secret', max_length=30, default='')

    class Meta:
        pass

    def __unicode__(self):
        return "Lab '{0}' - Console Server '{1}'".format(self.lab, self.name)


class Device(models.Model):
    pod = models.ForeignKey(Pod, related_name='devices')
    consoleserver = models.ForeignKey(ConsoleServer, related_name='devices')
    name = models.CharField('Name', max_length=30)

    class Meta:
        pass

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, related_name='memberships')
    lab = models.ForeignKey(Lab, related_name='memberships')
    role = models.PositiveSmallIntegerField('Role')

    class Meta:
        pass

    def __unicode__(self):
        return "{0} is a member of {1}".format(self.user, self.lab)
