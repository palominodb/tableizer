# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TableDefinition'
        db.create_table('table_definitions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('database_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('create_syntax', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['TableDefinition'])

        # Adding model 'TableVolume'
        db.create_table('table_volumes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('database_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('data_length', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('index_length', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('data_free', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['TableVolume'])

        # Adding model 'TableView'
        db.create_table('table_views', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('database_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('create_syntax', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['TableView'])

        # Adding model 'TableUser'
        db.create_table('table_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permtype', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('server', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Host', blank=True)),
            ('db', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Db', blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='User', blank=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Table_name', blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Password', blank=True)),
            ('column_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Column_name', blank=True)),
            ('routine_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Routine_name', blank=True)),
            ('routine_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Routine_type', blank=True)),
            ('grantor', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, db_column='Grantor', blank=True)),
            ('ssl_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('ssl_cipher', self.gf('django.db.models.fields.BinaryField')(default=None, null=True, blank=True)),
            ('x509_issuer', self.gf('django.db.models.fields.BinaryField')(default=None, null=True, blank=True)),
            ('x509_subject', self.gf('django.db.models.fields.BinaryField')(default=None, null=True, blank=True)),
            ('max_questions', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('max_updates', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('max_connections', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('max_user_connections', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('plugin', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('authentication_string', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('create_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_priv', blank=True)),
            ('drop_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Drop_priv', blank=True)),
            ('grant_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Grant_priv', blank=True)),
            ('references_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='References_priv', blank=True)),
            ('event_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Event_priv', blank=True)),
            ('alter_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Alter_priv', blank=True)),
            ('delete_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Delete_priv', blank=True)),
            ('index_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Index_priv', blank=True)),
            ('insert_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Insert_priv', blank=True)),
            ('select_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Select_priv', blank=True)),
            ('update_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Update_priv', blank=True)),
            ('create_tmp_table_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_tmp_table_priv', blank=True)),
            ('lock_tables_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Lock_tables_priv', blank=True)),
            ('trigger_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Trigger_priv', blank=True)),
            ('create_view_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_view_priv', blank=True)),
            ('show_view_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Show_view_priv', blank=True)),
            ('execute_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Execute_priv', blank=True)),
            ('file_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='File_priv', blank=True)),
            ('create_user_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_user_priv', blank=True)),
            ('process_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Process_priv', blank=True)),
            ('reload_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Reload_priv', blank=True)),
            ('repl_client_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Repl_client_priv', blank=True)),
            ('repl_slave_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Repl_slave_priv', blank=True)),
            ('create_routine_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_routine_priv', blank=True)),
            ('alter_routine_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Alter_routine_priv', blank=True)),
            ('create_tablespace_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Create_tablespace_priv', blank=True)),
            ('show_db_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Show_db_priv', blank=True)),
            ('shutdown_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Shutdown_priv', blank=True)),
            ('super_priv', self.gf('django.db.models.fields.CharField')(default=None, max_length=1, null=True, db_column='Super_priv', blank=True)),
            ('run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['TableUser'])

        # Adding model 'CollectorRun'
        db.create_table('collector_runs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collector', self.gf('django.db.models.fields.CharField')(default=None, max_length=25, null=True, blank=True)),
            ('last_run', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['CollectorRun'])

        # Adding model 'Server'
        db.create_table('servers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cached_size', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['Server'])

        # Adding model 'ServerSchema'
        db.create_table('server_schemas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ttt.Server'], null=True, blank=True)),
            ('cached_size', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['ServerSchema'])

        # Adding model 'DatabaseTable'
        db.create_table('database_tables', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ttt.ServerSchema'], null=True, blank=True)),
            ('cached_size', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['DatabaseTable'])

        # Adding model 'Snapshot'
        db.create_table('snapshots', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('txn', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('collector_run', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ttt.CollectorRun'], null=True, blank=True)),
            ('statistic_id', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('parent_txn', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('run_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'ttt', ['Snapshot'])


    def backwards(self, orm):
        # Deleting model 'TableDefinition'
        db.delete_table('table_definitions')

        # Deleting model 'TableVolume'
        db.delete_table('table_volumes')

        # Deleting model 'TableView'
        db.delete_table('table_views')

        # Deleting model 'TableUser'
        db.delete_table('table_users')

        # Deleting model 'CollectorRun'
        db.delete_table('collector_runs')

        # Deleting model 'Server'
        db.delete_table('servers')

        # Deleting model 'ServerSchema'
        db.delete_table('server_schemas')

        # Deleting model 'DatabaseTable'
        db.delete_table('database_tables')

        # Deleting model 'Snapshot'
        db.delete_table('snapshots')


    models = {
        u'ttt.collectorrun': {
            'Meta': {'object_name': 'CollectorRun', 'db_table': "'collector_runs'"},
            'collector': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.databasetable': {
            'Meta': {'ordering': "('-cached_size',)", 'object_name': 'DatabaseTable', 'db_table': "'database_tables'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['ttt.ServerSchema']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.server': {
            'Meta': {'ordering': "('-cached_size',)", 'object_name': 'Server', 'db_table': "'servers'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.serverschema': {
            'Meta': {'ordering': "('-cached_size',)", 'object_name': 'ServerSchema', 'db_table': "'server_schemas'"},
            'cached_size': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['ttt.Server']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.snapshot': {
            'Meta': {'object_name': 'Snapshot', 'db_table': "'snapshots'"},
            'collector_run': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['ttt.CollectorRun']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_txn': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'statistic_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'txn': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.tabledefinition': {
            'Meta': {'object_name': 'TableDefinition', 'db_table': "'table_definitions'"},
            'create_syntax': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.tables': {
            'Meta': {'unique_together': "(('table_schema', 'table_name'),)", 'object_name': 'Tables', 'db_table': "'TABLES'", 'managed': 'False'},
            'auto_increment': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'AUTO_INCREMENT'", 'blank': 'True'}),
            'avg_row_length': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'AVG_ROW_LENGTH'", 'blank': 'True'}),
            'check_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'CHECK_TIME'", 'blank': 'True'}),
            'checksum': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'CHECKSUM'", 'blank': 'True'}),
            'create_options': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'CREATE_OPTIONS'", 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'CREATE_TIME'", 'blank': 'True'}),
            'data_free': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'DATA_FREE'", 'blank': 'True'}),
            'data_length': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'DATA_LENGTH'", 'blank': 'True'}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'ENGINE'", 'blank': 'True'}),
            'index_length': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'INDEX_LENGTH'", 'blank': 'True'}),
            'max_data_length': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'MAX_DATA_LENGTH'", 'blank': 'True'}),
            'row_format': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ROW_FORMAT'", 'blank': 'True'}),
            'table_catalog': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_column': "'TABLE_CATALOG'"}),
            'table_collation': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'TABLE_COLLATION'", 'blank': 'True'}),
            'table_comment': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_column': "'TABLE_COMMENT'"}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True', 'db_column': "'TABLE_NAME'"}),
            'table_rows': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'TABLE_ROWS'", 'blank': 'True'}),
            'table_schema': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'TABLE_SCHEMA'"}),
            'table_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'TABLE_TYPE'"}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'UPDATE_TIME'", 'blank': 'True'}),
            'version': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_column': "'VERSION'", 'blank': 'True'})
        },
        u'ttt.tableuser': {
            'Meta': {'object_name': 'TableUser', 'db_table': "'table_users'"},
            'alter_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Alter_priv'", 'blank': 'True'}),
            'alter_routine_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Alter_routine_priv'", 'blank': 'True'}),
            'authentication_string': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'column_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Column_name'", 'blank': 'True'}),
            'create_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_priv'", 'blank': 'True'}),
            'create_routine_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_routine_priv'", 'blank': 'True'}),
            'create_tablespace_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_tablespace_priv'", 'blank': 'True'}),
            'create_tmp_table_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_tmp_table_priv'", 'blank': 'True'}),
            'create_user_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_user_priv'", 'blank': 'True'}),
            'create_view_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Create_view_priv'", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Db'", 'blank': 'True'}),
            'delete_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Delete_priv'", 'blank': 'True'}),
            'drop_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Drop_priv'", 'blank': 'True'}),
            'event_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Event_priv'", 'blank': 'True'}),
            'execute_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Execute_priv'", 'blank': 'True'}),
            'file_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'File_priv'", 'blank': 'True'}),
            'grant_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Grant_priv'", 'blank': 'True'}),
            'grantor': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Grantor'", 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Host'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Index_priv'", 'blank': 'True'}),
            'insert_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Insert_priv'", 'blank': 'True'}),
            'lock_tables_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Lock_tables_priv'", 'blank': 'True'}),
            'max_connections': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'max_questions': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'max_updates': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'max_user_connections': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Password'", 'blank': 'True'}),
            'permtype': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'process_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Process_priv'", 'blank': 'True'}),
            'references_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'References_priv'", 'blank': 'True'}),
            'reload_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Reload_priv'", 'blank': 'True'}),
            'repl_client_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Repl_client_priv'", 'blank': 'True'}),
            'repl_slave_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Repl_slave_priv'", 'blank': 'True'}),
            'routine_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Routine_name'", 'blank': 'True'}),
            'routine_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Routine_type'", 'blank': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'select_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Select_priv'", 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'show_db_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Show_db_priv'", 'blank': 'True'}),
            'show_view_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Show_view_priv'", 'blank': 'True'}),
            'shutdown_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Shutdown_priv'", 'blank': 'True'}),
            'ssl_cipher': ('django.db.models.fields.BinaryField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ssl_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'super_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Super_priv'", 'blank': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'Table_name'", 'blank': 'True'}),
            'trigger_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Trigger_priv'", 'blank': 'True'}),
            'update_priv': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'db_column': "'Update_priv'", 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'db_column': "'User'", 'blank': 'True'}),
            'x509_issuer': ('django.db.models.fields.BinaryField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'x509_subject': ('django.db.models.fields.BinaryField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.tableview': {
            'Meta': {'object_name': 'TableView', 'db_table': "'table_views'"},
            'create_syntax': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'ttt.tablevolume': {
            'Meta': {'object_name': 'TableVolume', 'db_table': "'table_volumes'"},
            'data_free': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'data_length': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_length': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'run_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'table_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ttt']