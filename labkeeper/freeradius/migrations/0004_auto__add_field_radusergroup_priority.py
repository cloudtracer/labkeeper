# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Radusergroup.priority'
        db.add_column('radusergroup', 'priority',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Radusergroup.priority'
        db.delete_column('radusergroup', 'priority')


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
        },
        u'freeradius.radusergroup': {
            'Meta': {'object_name': 'Radusergroup', 'db_table': "'radusergroup'"},
            'groupname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['freeradius']