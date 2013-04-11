# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_index('table_definitions', ['run_time'])
        db.create_index('table_definitions', ['server', 'database_name', 'table_name'])
        
        db.create_index('table_volumes', ['run_time'])
        db.create_index('table_volumes', ['server', 'database_name', 'table_name'])
        
        db.create_index('collector_runs', ['collector'], unique=True)
        
        db.create_index('servers', ['name'], unique=True)
        db.create_index('server_schemas', ['name'])
        db.create_index('database_tables', ['name'])
        
        db.create_index('snapshots', ['txn'])
        db.create_index('snapshots', ['collector_run_id'])
        db.create_index('snapshots', ['parent_txn'])
        
        db.create_index('snapshots', ['txn', 'collector_run_id'])
        db.create_index('snapshots', ['statistic_id', 'collector_run_id'])
        db.create_index('snapshots', ['run_time', 'collector_run_id'])

    def backwards(self, orm):
        db.delete_index('table_definitions', ['run_time'])
        db.delete_index('table_definitions', ['server', 'database_name', 'table_name'])
        
        db.delete_index('table_volumes', ['run_time'])
        db.delete_index('table_volumes', ['server', 'database_name', 'table_name'])
        
        db.delete_index('collector_runs', ['collector'])

        db.delete_index('servers', ['name'])
        db.delete_index('server_schemas', ['name'])
        db.delete_index('database_tables', ['name'])
        
        db.delete_index('snapshots', ['txn'])
        db.delete_index('snapshots', ['collector_run_id'])
        db.delete_index('snapshots', ['parent_txn'])
        
        db.delete_index('snapshots', ['txn', 'collector_run_id'])
        db.delete_index('snapshots', ['statistic_id', 'collector_run_id'])
        db.delete_index('snapshots', ['run_time', 'collector_run_id'])

    models = {
        u'ttt.tabledefinition': {
            'Meta': {'object_name': 'TableDefinition', 'db_table': "'table_definitions'"},
            'create_syntax': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ttt.tablevolume': {
            'Meta': {'object_name': 'TableVolume', 'db_table': "'table_volumes'"},
            'data_free': ('django.db.models.fields.IntegerField', [], {}),
            'data_length': ('django.db.models.fields.IntegerField', [], {}),
            'database_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_length': ('django.db.models.fields.IntegerField', [], {}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['ttt']
