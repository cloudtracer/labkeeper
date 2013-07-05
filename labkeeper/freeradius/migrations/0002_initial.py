# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Radcheck'
        db.create_table('radcheck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('op', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=253)),
        ))
        db.send_create_signal(u'freeradius', ['Radcheck'])

        # Adding model 'Radreply'
        db.create_table('radreply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('op', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=253)),
        ))
        db.send_create_signal(u'freeradius', ['Radreply'])


    def backwards(self, orm):
        # Deleting model 'Radcheck'
        db.delete_table('radcheck')

        # Deleting model 'Radreply'
        db.delete_table('radreply')


    models = {
        u'freeradius.radcheck': {
            'Meta': {'object_name': 'Radcheck', 'db_table': "'radcheck'"},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'op': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '253'})
        },
        u'freeradius.radreply': {
            'Meta': {'object_name': 'Radreply', 'db_table': "'radreply'"},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'op': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '253'})
        }
    }

    complete_apps = ['freeradius']