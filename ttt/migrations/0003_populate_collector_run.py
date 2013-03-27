# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from ttt.collector import CollectorRegistry

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        CollectorRegistry.load()
        for collector in CollectorRegistry.all():
            orm['ttt.CollectorRun'].objects.get_or_create(collector=collector.id, last_run=None)

    def backwards(self, orm):
        "Write your backwards methods here."
        orm['ttt.CollectorRun'].objects.all().delete()

    models = {
        u'ttt.collectorrun': {
            'Meta': {'object_name': 'CollectorRun', 'db_table': "'collector_runs'"},
            'collector': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'ttt.databasetable': {
            'Meta': {'object_name': 'DatabaseTable', 'db_table': "'database_tables'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttt.ServerSchema']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ttt.server': {
            'Meta': {'object_name': 'Server', 'db_table': "'servers'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ttt.serverschema': {
            'Meta': {'object_name': 'ServerSchema', 'db_table': "'server_schemas'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttt.Server']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ttt.snapshot': {
            'Meta': {'object_name': 'Snapshot', 'db_table': "'snapshots'"},
            'collector_run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttt.CollectorRun']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_txn': ('django.db.models.fields.IntegerField', [], {}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'statistic_id': ('django.db.models.fields.IntegerField', [], {}),
            'txn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ttt.tabledefinition': {
            'Meta': {'object_name': 'TableDefinition', 'db_table': "'table_definitions'"},
            'create_syntax': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.tableuser': {
            'Alter_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Column_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'Create_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Create_tmp_table_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Create_user_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Create_view_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Db': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'Delete_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Drop_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Event_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Execute_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'File_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Grant_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Grantor': ('django.db.models.fields.CharField', [], {'max_length': '92'}),
            'Host': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Index_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Insert_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Lock_tables_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Meta': {'object_name': 'TableUser', 'db_table': "'table_users'"},
            'Password': ('django.db.models.fields.CharField', [], {'max_length': '41'}),
            'Process_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'References_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Reload_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Repl_client_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Repl_slave_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Routine_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'Routine_type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'Select_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Show_db_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Shutdown_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Super_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'Trigger_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Update_priv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'User': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_connections': ('django.db.models.fields.IntegerField', [], {}),
            'max_questions': ('django.db.models.fields.IntegerField', [], {}),
            'max_updates': ('django.db.models.fields.IntegerField', [], {}),
            'max_user_connections': ('django.db.models.fields.IntegerField', [], {}),
            'permtype': ('django.db.models.fields.IntegerField', [], {}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ssl_cipher': ('django.db.models.fields.BinaryField', [], {}),
            'ssl_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'x509_issuer': ('django.db.models.fields.BinaryField', [], {}),
            'x509_subject': ('django.db.models.fields.BinaryField', [], {})
        },
        u'ttt.tableview': {
            'Meta': {'object_name': 'TableView', 'db_table': "'table_views'"},
            'create_syntax': ('django.db.models.fields.TextField', [], {}),
            'database_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
    symmetrical = True
