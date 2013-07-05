from django.db import models


# http://wiki.freeradius.org/config/Operators
RADIUS_CHECK_OPS = (
    ('=', '='),
    (':=', ':='),
    ('==', '=='),
    ('+=', '+='),
    ('!=', '!='),
    ('>', '>'),
    ('>=', '>='),
    ('<', '<'),
    ('<=', '<='),
    ('=~', '=~'),
    ('!~', '!~'),
    ('=*', '=*'),
    ('!*', '!*'),
)
RADIUS_REPLY_OPS = (
    ('=', '='),
    (':=', ':='),
    ('+=', '+='),
)

class Radcheck(models.Model):
    username = models.CharField('Username', max_length=32)
    attribute = models.CharField('Attribute', max_length=32)
    op = models.CharField('Operator', max_length=2, choices=RADIUS_CHECK_OPS)
    value = models.CharField('Value', max_length=253)

    class Meta:
        db_table = 'radcheck'

    def __unicode__(self):
        return '{0}: {1} {2} {3}'.format(self.username, self.attribute, self.op, self.value)

class Radreply(models.Model):
    username = models.CharField('Username', max_length=32)
    attribute = models.CharField('Attribute', max_length=32)
    op = models.CharField('Operator', max_length=2, choices=RADIUS_REPLY_OPS)
    value = models.CharField('Value', max_length=253)

    class Meta:
        db_table = 'radreply'
        verbose_name_plural = 'radreplies'

    def __unicode__(self):
        return '{0}: {1} {2} {3}'.format(self.username, self.attribute, self.op, self.value)

# Dummy table required by freeradius
class Radusergroup(models.Model):
    username = models.CharField('Username', max_length=32)
    groupname = models.CharField('Groupname', max_length=32)
    priority = models.PositiveIntegerField('Priority', default=0)

    class Meta:
        db_table = 'radusergroup'
        verbose_name_plural = 'radusergroups'

    def __unicode__(self):
        return '{0} assigned to group {1}'.format(self.username, self.groupname)
