# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Membership'
        db.create_table(u'labs_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['auth.User'])),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['labs.Lab'])),
            ('role', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'labs', ['Membership'])

        # Adding model 'Pod'
        db.create_table(u'labs_pod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pods', to=orm['labs.Lab'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='Default', max_length=80)),
        ))
        db.send_create_signal(u'labs', ['Pod'])

        # Adding model 'Device'
        db.create_table(u'labs_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pod', self.gf('django.db.models.fields.related.ForeignKey')(related_name='devices', to=orm['labs.Pod'])),
            ('consoleserver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='devices', to=orm['labs.ConsoleServer'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'labs', ['Device'])

        # Adding model 'ConsoleServer'
        db.create_table(u'labs_consoleserver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consoleservers', to=orm['labs.Lab'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'labs', ['ConsoleServer'])

        # Adding model 'Lab'
        db.create_table(u'labs_lab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'labs', ['Lab'])


    def backwards(self, orm):
        # Deleting model 'Membership'
        db.delete_table(u'labs_membership')

        # Deleting model 'Pod'
        db.delete_table(u'labs_pod')

        # Deleting model 'Device'
        db.delete_table(u'labs_device')

        # Deleting model 'ConsoleServer'
        db.delete_table(u'labs_consoleserver')

        # Deleting model 'Lab'
        db.delete_table(u'labs_lab')


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
            'Meta': {'object_name': 'ConsoleServer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consoleservers'", 'to': u"orm['labs.Lab']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'labs.device': {
            'Meta': {'object_name': 'Device'},
            'consoleserver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'to': u"orm['labs.ConsoleServer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'to': u"orm['labs.Pod']"})
        },
        u'labs.lab': {
            'Meta': {'object_name': 'Lab'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'labs.membership': {
            'Meta': {'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['labs.Lab']"}),
            'role': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['auth.User']"})
        },
        u'labs.pod': {
            'Meta': {'object_name': 'Pod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pods'", 'to': u"orm['labs.Lab']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default'", 'max_length': '80'})
        }
    }

    complete_apps = ['labs']