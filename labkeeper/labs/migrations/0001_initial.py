# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lab'
        db.create_table(u'labs_lab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('founded', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_multipod', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_rsv_per_user', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('opening_time', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('closing_time', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('min_reservation', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('max_reservation', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=6)),
            ('photo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('profile', self.gf('django_bleach.models.BleachField')()),
            ('last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_edited_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'labs', ['Lab'])

        # Adding model 'Topology'
        db.create_table(u'labs_topology', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topologies', to=orm['labs.Lab'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topologies', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'labs', ['Topology'])

        # Adding unique constraint on 'Topology', fields ['lab', 'image']
        db.create_unique(u'labs_topology', ['lab_id', 'image'])

        # Adding model 'Pod'
        db.create_table(u'labs_pod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pods', to=orm['labs.Lab'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=30)),
        ))
        db.send_create_signal(u'labs', ['Pod'])

        # Adding unique constraint on 'Pod', fields ['lab', 'name']
        db.create_unique(u'labs_pod', ['lab_id', 'name'])

        # Adding model 'ConsoleServer'
        db.create_table(u'labs_consoleserver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consoleservers', to=orm['labs.Lab'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('fqdn', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('ip4_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, unique=True, null=True, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
        ))
        db.send_create_signal(u'labs', ['ConsoleServer'])

        # Adding unique constraint on 'ConsoleServer', fields ['lab', 'ip4_address']
        db.create_unique(u'labs_consoleserver', ['lab_id', 'ip4_address'])

        # Adding model 'ConsoleServerPort'
        db.create_table(u'labs_consoleserverport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consoleserver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ports', to=orm['labs.ConsoleServer'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('telnet_port', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('ssh_port', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'labs', ['ConsoleServerPort'])

        # Adding unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'number']
        db.create_unique(u'labs_consoleserverport', ['consoleserver_id', 'number'])

        # Adding unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'telnet_port']
        db.create_unique(u'labs_consoleserverport', ['consoleserver_id', 'telnet_port'])

        # Adding unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'ssh_port']
        db.create_unique(u'labs_consoleserverport', ['consoleserver_id', 'ssh_port'])

        # Adding model 'Device'
        db.create_table(u'labs_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(related_name='devices', to=orm['labs.Pod'])),
            ('cs_port', self.gf('django.db.models.fields.related.OneToOneField')(related_name='device', unique=True, to=orm['labs.ConsoleServerPort'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=30)),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
        ))
        db.send_create_signal(u'labs', ['Device'])

        # Adding unique constraint on 'Device', fields ['pod', 'name']
        db.create_unique(u'labs_device', ['pod_id', 'name'])

        # Adding unique constraint on 'Device', fields ['pod', 'slug']
        db.create_unique(u'labs_device', ['pod_id', 'slug'])

        # Adding model 'Membership'
        db.create_table(u'labs_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['auth.User'])),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['labs.Lab'])),
            ('role', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('joined', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'labs', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['user', 'lab']
        db.create_unique(u'labs_membership', ['user_id', 'lab_id'])

        # Adding model 'MembershipInvitation'
        db.create_table(u'labs_membershipinvitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_invitations', to=orm['auth.User'])),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_invitations', to=orm['labs.Lab'])),
            ('sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'labs', ['MembershipInvitation'])

        # Adding unique constraint on 'MembershipInvitation', fields ['recipient', 'lab']
        db.create_unique(u'labs_membershipinvitation', ['recipient_id', 'lab_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MembershipInvitation', fields ['recipient', 'lab']
        db.delete_unique(u'labs_membershipinvitation', ['recipient_id', 'lab_id'])

        # Removing unique constraint on 'Membership', fields ['user', 'lab']
        db.delete_unique(u'labs_membership', ['user_id', 'lab_id'])

        # Removing unique constraint on 'Device', fields ['pod', 'slug']
        db.delete_unique(u'labs_device', ['pod_id', 'slug'])

        # Removing unique constraint on 'Device', fields ['pod', 'name']
        db.delete_unique(u'labs_device', ['pod_id', 'name'])

        # Removing unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'ssh_port']
        db.delete_unique(u'labs_consoleserverport', ['consoleserver_id', 'ssh_port'])

        # Removing unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'telnet_port']
        db.delete_unique(u'labs_consoleserverport', ['consoleserver_id', 'telnet_port'])

        # Removing unique constraint on 'ConsoleServerPort', fields ['consoleserver', 'number']
        db.delete_unique(u'labs_consoleserverport', ['consoleserver_id', 'number'])

        # Removing unique constraint on 'ConsoleServer', fields ['lab', 'ip4_address']
        db.delete_unique(u'labs_consoleserver', ['lab_id', 'ip4_address'])

        # Removing unique constraint on 'Pod', fields ['lab', 'name']
        db.delete_unique(u'labs_pod', ['lab_id', 'name'])

        # Removing unique constraint on 'Topology', fields ['lab', 'image']
        db.delete_unique(u'labs_topology', ['lab_id', 'image'])

        # Deleting model 'Lab'
        db.delete_table(u'labs_lab')

        # Deleting model 'Topology'
        db.delete_table(u'labs_topology')

        # Deleting model 'Pod'
        db.delete_table(u'labs_pod')

        # Deleting model 'ConsoleServer'
        db.delete_table(u'labs_consoleserver')

        # Deleting model 'ConsoleServerPort'
        db.delete_table(u'labs_consoleserverport')

        # Deleting model 'Device'
        db.delete_table(u'labs_device')

        # Deleting model 'Membership'
        db.delete_table(u'labs_membership')

        # Deleting model 'MembershipInvitation'
        db.delete_table(u'labs_membershipinvitation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'labs.consoleserver': {
            'Meta': {'unique_together': "(('lab', 'ip4_address'),)", 'object_name': 'ConsoleServer'},
            'fqdn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip4_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consoleservers'", 'to': u"orm['labs.Lab']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'labs.consoleserverport': {
            'Meta': {'unique_together': "(('consoleserver', 'number'), ('consoleserver', 'telnet_port'), ('consoleserver', 'ssh_port'))", 'object_name': 'ConsoleServerPort'},
            'consoleserver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ports'", 'to': u"orm['labs.ConsoleServer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ssh_port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telnet_port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'labs.device': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('pod', 'name'), ('pod', 'slug'))", 'object_name': 'Device'},
            'cs_port': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'device'", 'unique': 'True', 'to': u"orm['labs.ConsoleServerPort']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'to': u"orm['labs.Pod']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'labs.lab': {
            'Meta': {'object_name': 'Lab'},
            'allow_multipod': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'closing_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'founded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_edited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'max_reservation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '6'}),
            'max_rsv_per_user': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'min_reservation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'opening_time': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'profile': ('django_bleach.models.BleachField', [], {})
        },
        u'labs.membership': {
            'Meta': {'unique_together': "(('user', 'lab'),)", 'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['labs.Lab']"}),
            'role': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['auth.User']"})
        },
        u'labs.membershipinvitation': {
            'Meta': {'unique_together': "(('recipient', 'lab'),)", 'object_name': 'MembershipInvitation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_invitations'", 'to': u"orm['labs.Lab']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_invitations'", 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'labs.pod': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('lab', 'name'),)", 'object_name': 'Pod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pods'", 'to': u"orm['labs.Lab']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30'})
        },
        u'labs.topology': {
            'Meta': {'ordering': "['title']", 'unique_together': "(('lab', 'image'),)", 'object_name': 'Topology'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topologies'", 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topologies'", 'to': u"orm['labs.Lab']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['labs']