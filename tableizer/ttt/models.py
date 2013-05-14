# models.py
# Copyright (C) 2009-2013 PalominoDB, Inc.
# 
# You may contact the maintainers at eng@palominodb.com.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import re
import time
from datetime import datetime

from django.db import connections, models
from django.db.models.signals import class_prepared
from django.dispatch import receiver

import managers
from utilities.utils import get_db_key

# TrackingTable Mixin
class TrackingTable(models.Model):
    __tables = {}

    class Meta:
        abstract = True

    @property
    def collector_id(self):
        CollectorRun = models.get_model('ttt', 'CollectorRun')
        return CollectorRun.objects.get_or_create(collector=self.collector)[0].id
        
    @property
    def status(self):
        status = self.__class__.objects.status(self)
        return status
        
    @property
    def previous_version(self):
        return self.__class__.objects.previous_version(self)
        
    @property
    def deleted(self):
        return self.__class__.objects.deleted(self)
        
    @property
    def unreachable(self):
        return self.__class__.objects.unreachable(self)
        
    @property
    def tchanged(self):
        return self.__class__.objects.tchanged(self)
        
    @property
    def new(self):
        return self.__class__.objects.new(self)
        
    
    @property
    def server_id(self):
        Server = models.get_model('ttt', 'Server')
        return Server.objects.get(name=self.server).id
        
    @property
    def db_id(self):
        ServerSchema = models.get_model('ttt', 'ServerSchema')
        return ServerSchema.objects.get(name=self.database_name, server__name=self.server).id
        
    @property
    def table_id(self):
        DatabaseTable = models.get_model('ttt', 'DatabaseTable')
        return DatabaseTable.objects.get(name=self.table_name, schema__name=self.database_name, schema__server__name=self.server).id

    def history(self, since=datetime.fromtimestamp(time.mktime([0,0,0,0,0,0,0,0,0]))):
        return self.__class__.objects.history(self, since)

@receiver(class_prepared)
def class_prepared_handler(sender, **kwargs):
    try:
        TrackingTable._TrackingTable__tables[sender.collector] = sender
    except Exception, e:
        pass


class TableDefinition(TrackingTable):
    server = models.CharField(max_length=100, null=True, blank=True, default=None)
    database_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    table_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    create_syntax = models.TextField(null=True, blank=True, default=None)
    run_time = models.DateTimeField(null=True, blank=True, default=None)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    collector = 'definition'
    objects = managers.TableDefinitionManager()
    
    class Meta:
        db_table = 'table_definitions'
        index_together = (
            ('run_time',),
            ('server', 'database_name', 'table_name'),
        )
        
    @property
    def stat_created_at(self):
        return self.created_at
    
    @property
    def prev_stat_created_at(self):
        return self.previous_version.created_at if self.previous_version is not None else ''
        
class TableVolume(TrackingTable):
    server = models.CharField(max_length=100, null=True, blank=True, default=None)
    database_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    table_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    data_length = models.BigIntegerField(null=True, blank=True, default=None)
    index_length = models.BigIntegerField(null=True, blank=True, default=None)
    data_free = models.BigIntegerField(null=True, blank=True, default=None)
    run_time = models.DateTimeField(null=True, blank=True, default=None)
    
    collector = 'volume'
    objects = managers.TableVolumeManager()
    
    class Meta:
        db_table = 'table_volumes'
        index_together = (
            ('run_time',),
            ('server', 'database_name', 'table_name'),
        )
    
    @property    
    def size(self):
        if self.data_length is not None and self.index_length is not None:
            return self.data_length + self.index_length
        else:
            return None
    
    def save(self, *args, **kwargs):
        super(TableVolume, self).save(*args, **kwargs)
        self.__update_cached_table_size()
    
    def __update_cached_table_size(self):
        s = Server.objects.find_by_name(self.server)
        if s is not None:
            sch = s.serverschema_set.find_by_name(self.database_name)
        if sch is not None:
            t = sch.databasetable_set.find_by_name(self.table_name)
            t.cached_size = self.size
            t.save()
        
class TableView(TrackingTable):
    server = models.CharField(max_length=100, null=True, blank=True, default=None)
    database_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    table_name = models.CharField(max_length=64, null=True, blank=True, default=None)
    create_syntax = models.TextField(null=True, blank=True, default=None)
    run_time = models.DateTimeField(null=True, blank=True, default=None)
    
    collector = 'view'
    objects = managers.TableViewManager()
    
    class Meta:
        db_table = 'table_views'
        
    @property
    def created_at(self):
        return self.run_time
        
    @property
    def stat_created_at(self):
        return self.created_at
    
    @property
    def prev_stat_created_at(self):
        return self.previous_version.created_at if self.previous_version is not None else ''
        
class TableUser(TrackingTable):
    permtype = models.IntegerField(null=True, blank=True, default=None)
    server = models.CharField(max_length=255, null=True, blank=True, default=None)
    host = models.CharField(db_column='Host', max_length=255, null=True, blank=True, default=None)
    db = models.CharField(db_column='Db', max_length=255, null=True, blank=True, default=None)
    user = models.CharField(db_column='User', max_length=255, null=True, blank=True, default=None)
    table_name = models.CharField(db_column='Table_name', max_length=255, null=True, blank=True, default=None)
    password = models.CharField(db_column='Password', max_length=255, null=True, blank=True, default=None)
    column_name = models.CharField(db_column='Column_name', max_length=255, null=True, blank=True, default=None)
    routine_name = models.CharField(db_column='Routine_name', max_length=255, null=True, blank=True, default=None)
    routine_type = models.CharField(db_column='Routine_type', max_length=255, null=True, blank=True, default=None)
    grantor = models.CharField(db_column='Grantor', max_length=255, null=True, blank=True, default=None)
    ssl_type = models.CharField(max_length=20, null=True, blank=True, default=None)
    ssl_cipher = models.BinaryField(null=True, blank=True, default=None)
    x509_issuer = models.BinaryField(null=True, blank=True, default=None)
    x509_subject = models.BinaryField(null=True, blank=True, default=None)
    max_questions = models.IntegerField(null=True, blank=True, default=None)
    max_updates = models.IntegerField(null=True, blank=True, default=None)
    max_connections = models.IntegerField(null=True, blank=True, default=None)
    max_user_connections = models.IntegerField(null=True, blank=True, default=None)
    plugin = models.CharField(max_length=64, null=True, blank=True, default=None)
    authentication_string = models.TextField(null=True, blank=True, default=None)
    
    #Privs
    create_priv = models.CharField(db_column='Create_priv', max_length=1, null=True, blank=True, default=None)
    drop_priv = models.CharField(db_column='Drop_priv', max_length=1, null=True, blank=True, default=None)
    grant_priv = models.CharField(db_column='Grant_priv', max_length=1, null=True, blank=True, default=None)
    references_priv = models.CharField(db_column='References_priv', max_length=1, null=True, blank=True, default=None)
    event_priv = models.CharField(db_column='Event_priv', max_length=1, null=True, blank=True, default=None)
    alter_priv = models.CharField(db_column='Alter_priv', max_length=1, null=True, blank=True, default=None)
    delete_priv = models.CharField(db_column='Delete_priv', max_length=1, null=True, blank=True, default=None)
    index_priv = models.CharField(db_column='Index_priv', max_length=1, null=True, blank=True, default=None)
    insert_priv = models.CharField(db_column='Insert_priv', max_length=1, null=True, blank=True, default=None)
    select_priv = models.CharField(db_column='Select_priv', max_length=1, null=True, blank=True, default=None)
    update_priv = models.CharField(db_column='Update_priv', max_length=1, null=True, blank=True, default=None)
    create_tmp_table_priv = models.CharField(db_column='Create_tmp_table_priv', max_length=1, null=True, blank=True, default=None)
    lock_tables_priv = models.CharField(db_column='Lock_tables_priv', max_length=1, null=True, blank=True, default=None)
    trigger_priv = models.CharField(db_column='Trigger_priv', max_length=1, null=True, blank=True, default=None)
    create_view_priv = models.CharField(db_column='Create_view_priv', max_length=1, null=True, blank=True, default=None)
    show_view_priv = models.CharField(db_column='Show_view_priv', max_length=1, null=True, blank=True, default=None)
    execute_priv = models.CharField(db_column='Execute_priv', max_length=1, null=True, blank=True, default=None)
    file_priv = models.CharField(db_column='File_priv', max_length=1, null=True, blank=True, default=None)
    create_user_priv = models.CharField(db_column='Create_user_priv', max_length=1, null=True, blank=True, default=None)
    process_priv = models.CharField(db_column='Process_priv', max_length=1, null=True, blank=True, default=None)
    reload_priv = models.CharField(db_column='Reload_priv', max_length=1, null=True, blank=True, default=None)
    repl_client_priv = models.CharField(db_column='Repl_client_priv', max_length=1, null=True, blank=True, default=None)
    repl_slave_priv = models.CharField(db_column='Repl_slave_priv', max_length=1, null=True, blank=True, default=None)
    create_routine_priv = models.CharField(db_column='Create_routine_priv', max_length=1, null=True, blank=True, default=None)
    alter_routine_priv = models.CharField(db_column='Alter_routine_priv', max_length=1, null=True, blank=True, default=None)
    create_tablespace_priv = models.CharField(db_column='Create_tablespace_priv', max_length=1, null=True, blank=True, default=None)
    show_db_priv = models.CharField(db_column='Show_db_priv', max_length=1, null=True, blank=True, default=None)
    shutdown_priv = models.CharField(db_column='Shutdown_priv', max_length=1, null=True, blank=True, default=None)
    super_priv = models.CharField(db_column='Super_priv', max_length=1, null=True, blank=True, default=None)
    
    run_time = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    collector = 'user'
    objects = managers.TableUserManager()
    
    class Meta:
        db_table = 'table_users'
        
    # Yeah, I know that bitmaps in a database are sorta a 'no no'
    # But, I think in this instance it's worth the trouble.

    # Mapping to the permtype column
    # This is less involved than 'computing' the permission type.
    GLOBAL_PERMISSION = 1<<4
    HOST_PERMISSION   = 1<<5
    DB_PERMISSION     = 1<<6
    TABLE_PERMISSION  = 1<<7
    COLUMN_PERMISSION = 1<<8
    PROC_PERMISSION   = 1<<9

    # This is or-ed with the above to mark a permission as deleted.
    DELETED_PERMISSION = 1<<1
    # These two bits are reserved for later use.
    UNREACHABLE_ENTRY  = 1<<2
    RESERVED_PERMISSION2 = 1<<3
    
    PRIV_FLAG_COLUMNS = [
        'create_priv', 'drop_priv', 'grant_priv', 'references_priv',
        'event_priv', 'alter_priv', 'delete_priv', 'index_priv', 'insert_priv', 'select_priv',
        'update_priv', 'create_tmp_table_priv', 'lock_tables_priv', 'trigger_priv',
        'create_view_priv', 'show_view_priv', 'execute_priv', 'file_priv', 'create_user_priv',
        'process_priv', 'reload_priv', 'repl_client_priv', 'repl_slave_priv', 'create_routine_priv',
        'alter_routine_priv', 'create_tablespace_priv', 'show_db_priv', 'shutdown_priv',
        'super_priv',
    ]
    
    ALL_GLOBAL_PRIVS = [
        'select_priv', 'insert_priv', 'update_priv', 'delete_priv', 'create_priv',
        'drop_priv', 'reload_priv', 'shutdown_priv', 'process_priv', 'file_priv',
        'grant_priv', 'references_priv', 'index_priv','alter_priv', 'show_db_priv',
        'create_tmp_table_priv', 'lock_tables_priv', 'execute_priv', 'repl_slave_priv',
        'repl_client_priv', 'create_view_priv', 'show_view_priv', 'create_routine_priv',
        'alter_routine_priv', 'create_user_priv', 'event_priv', 'trigger_priv',
        'create_tablespace_priv',
    ]
    
    ALL_DB_PRIVS = [
        'select_priv', 'insert_priv', 'update_priv', 'delete_priv', 'create_priv',
        'drop_priv', 'grant_priv', 'references_priv', 'index_priv', 'alter_priv',
        'create_tmp_table_priv', 'lock_tables_priv', 'create_view_priv',
        'show_view_priv', 'create_routine_priv', 'alter_routine_priv', 'execute_priv',
        'event_priv', 'trigger_priv',
    ]
    
    ALL_HOST_PRIVS = [
        'select_priv', 'insert_priv', 'update_priv', 'delete_priv', 'create_priv',
        'drop_priv', 'grant_priv', 'references_priv', 'index_priv', 'alter_priv',
        'create_tmp_table_priv', 'lock_tables_priv', 'create_view_priv',
        'show_view_priv', 'create_routine_priv', 'alter_routine_priv', 'execute_priv',
        'trigger_priv',
    ]
    
    ALL_TABLE_PRIVS = [
        'select_priv', 'insert_priv', 'update_priv', 'delete_priv', 'create_priv',
        'drop_priv', 'references_priv', 'index_priv', 'alter_priv', 'create_view_priv',
        'show_priv', 'trigger_priv',
    ]
    
    ALL_COLUMN_PRIVS = [
        'select_priv', 'insert_priv', 'update_priv', 'references_priv',
    ]
    
    ALL_PROC_PRIVS = [
        'execute_priv', 'alter_routine_priv', 'grant_priv',
    ]
    
    def __unicode__(self):
        gstr = 'GRANT '
        perms = self.perms_set.copy()
        if 'grant_priv' in perms:
            perms.remove('grant_priv')
        has_grant = 'grant_priv' in self.perms_set
        pw = '' if self.password is None or len(self.password) == 0 else 'IDENTIFIED BY PASSWORD \'%s\'' % (self.password)
        on_ref = 'ON *.*'
        user_ref = "'%s'@'%s'" % (self.user, '%' if self.host is None or len(self.host) == 0 else self.host)
        priv_message = lambda pstr: pstr
        if self.permtype & ~0x3 == self.GLOBAL_PERMISSION:
            privstype_set = set(self.ALL_GLOBAL_PRIVS)
        elif self.permtype & ~0x3 == self.HOST_PERMISSION:
            if self.deleted(self):
                return "DELETE FROM `mysql`.`host` WHERE HOST='%s' AND Db='%s'" % (self.host, self.db)
            else:
                return "REPLACE INTO `mysql`.`host` (Host,Db,%s) VALUES (%s,%s,%s)" % (','.join(sorted(list(perms))),
                                                                                        self.host if self.host is not None else '',
                                                                                        self.db if self.db is not None else '',
                                                                                        ','.join(map(lambda x: 'Y', sorted(list(perms)))))
        elif self.permtype & ~0x3 == self.DB_PERMISSION:
            on_ref = "ON `%s`.*" % (self.db)
            privstype_set = set(self.ALL_DB_PRIVS)
        elif self.permtype & ~0x3 == self.TABLE_PERMISSION:
            on_ref = "ON `%s`.`%s`" % (self.db if self.db is not None else '',
                                        self.table_name if self.table_name is not None else '')
            privstype_set = set(self.ALL_TABLE_PRIVS)
        elif self.permtype & ~0x3 == self.COLUMN_PERMISSION:
            on_ref = "ON `%s`.`%s`" % (self.db if self.db is not None else '',
                                        self.table_name if self.table_name is not None else '')
            privstype_set = set(self.ALL_COLUMN_PRIVS)
        elif self.permtype & ~0x3 == self.PROC_PERMISSION:
            privstype_set = set(self.ALL_PROC_PRIVS)
            
        if perms.issuperset(privstype_set):
            gstr += priv_message('ALL PRIVILEGES') + ' '
        elif len(perms) == 0:
            gstr += 'USAGE '
        else:
            gstr += ' '.join(map(lambda x: priv_message(self.perm_to_s(x)), perms))
        gstr += ', '.join([on_ref, 'TO', user_ref, pw, 'WITH GRANT OPTION' if has_grant else '']) + ' '
        if self.deleted:
            return 'DROP USER %s' % (user_ref)
        else:
            return gstr
    
    @property
    def database_name(self):
        return str(self.db)
        
    # Returns permissions as a set
    @property
    def perms_set(self):
        return set(filter(lambda x: getattr(self, x) == 'Y', self.PRIV_FLAG_COLUMNS))
        
    # Sets permissions from a set
    def perms_from_set(self, s):
        if not set(s).issubset(set(self.PRIV_FLAG_COLUMNS)):
            raise Exception, 'Invalid columns'
        map(lambda x: setattr(self, x, 'Y'), s)
        self.save()
        return True
        
    # Sets permissions from a comma separated set string
    def perms_from_setstr(self, s):
        return self.perm_from_set(set(map(lambda x: (x.replace(' ', '_') + '_priv').lower(), s.split(','))))
    
    def perm_to_s(self, perm):
        return perm.upper().replace('_', ' ').replace(' PRIV', '').replace('REPL', 'REPLICATION').replace('TMP TABLE', 'TEMPORARY TABLES')
    
    @classmethod
    def perms_from_setstr(cls, s):
        sn = set(map(lambda x: (x.replace(' ', '_') + '_priv').lower(), s.split(',')))
        if not set(sn).issubset(set(cls.PRIV_FLAG_COLUMNS)):
            raise Exception, 'Invalid columns'
        return sn
    
    @property
    def global_perm(self):
        return self.permtype & self.GLOBAL_PERMISSION != 0

    @property
    def host_perm(self):
        return self.permtype & self.HOST_PERMISSION != 0
        
    @property
    def db_perm(self):
        return self.permtype & self.DB_PERMISSION != 0

    @property
    def table_perm(self):
        return self.permtype & self.TABLE_PERMISSION != 0

    @property
    def column_perm(self):
        return self.permtype & self.COLUMN_PERMISSION != 0

    @property
    def proc_perm(self):
        return self.permtype & self.PROC_PERMISSION != 0

class CollectorRun(models.Model):
    collector = models.CharField(max_length=25, null=True, blank=True, default=None)
    last_run = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'collector_runs'
        index_together = (
            ('collector',),
        )
        
class Server(models.Model):
    name = models.CharField(max_length=100, null=False)
    cached_size = models.BigIntegerField(null=True, blank=True, default=None)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    objects = managers.ServerManager()

    class Meta:
        db_table = 'servers'
        ordering = ('-cached_size',)
        index_together = (
            ('name',),
        )
        
class ServerSchema(models.Model):
    name = models.CharField(max_length=64, null=False)
    server = models.ForeignKey(Server, null=True, blank=True, default=None)
    cached_size = models.BigIntegerField(null=True, blank=True, default=None)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    objects = managers.ServerSchemaManager()
    
    class Meta:
        db_table = 'server_schemas'
        ordering = ('-cached_size',)
        index_together = (
            ('name',),
        )
        
class DatabaseTable(models.Model):
    name = models.CharField(max_length=64, null=False)
    schema = models.ForeignKey(ServerSchema, null=True, blank=True, default=None)
    cached_size = models.BigIntegerField(null=True, blank=True, default=None)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    objects = managers.DatabaseTableManager()
        
    class Meta:
        db_table = 'database_tables'
        ordering = ('-cached_size',)
        index_together = (
            ('name',),
        )
        
    @property
    def table_name(self):
        return self.name
    
    @property
    def stats(self):
        stat_dict = {}
        for t in [TableDefinition, TableVolume, TableView, TableUser]:
            if t != TableUser:
                objects = t.objects.filter(server=self.schema.server.name, database_name=self.schema.name,
                                            table_name=self.name).order_by('-id')
            else:
                objects = t.objects.filter(server=self.schema.server.name, db=self.schema.name,
                                            table_name=self.name).order_by('-id')
            if objects.count() > 0:
                stat_dict[t.collector] = objects[0]
            else:
                stat_dict[t.collector] = None
        return stat_dict
    
    @property
    def has_stats(self):
        return self.stats.get('definition') is not None or self.stats.get('volume')  is not None \
            or self.stats.get('view')
    
    @property
    def table_type(self):
        type_ = 'base'
        if self.stats.get('definition') is None and self.stats.get('view') is None:
            type_ = 'unknown'
        elif self.stats.get('definition') is None and self.stats.get('view') is not None:
            type_ = 'view'
        return type_
    
    @property
    def create_syntax(self):
        return self.get_create()
    
    @property
    def stat_created_at(self):
        try:
            return self.stats.get('definition').created_at if self.table_type == 'base' else self.stats.get('view').run_time
        except Exception:
            return ''
    
    @property
    def prev_stat_created_at(self):
        try:
            return self.previous_version.created_at if self.table_type == 'base' else self.previous_version.run_time
        except Exception:
            return ''
    
    @property
    def previous_version(self):
        return self.stats.get('definition').previous_version if self.table_type == 'base' else self.stats.get('view').previous_version
        
    def get_create(self):
        if self.table_type == 'base':
            return self.stats.get('definition').create_syntax
        elif self.table_type == 'view':
            return self.stats.get('view').create_syntax
        else:
            return None
            
    def get_history(self, since=datetime.fromtimestamp(time.mktime([0,0,0,0,0,0,0,0,0]))):
        r = {}
        for k,v in self.stats.items():
            if v is not None:
                r[k] = v.history(since=since)
        return r
        
class Snapshot(models.Model):
    txn = models.IntegerField(null=True, blank=True, default=None)
    collector_run = models.ForeignKey(CollectorRun, null=True, blank=True, default=None)
    statistic_id = models.IntegerField(null=True, blank=True, default=None)
    parent_txn = models.IntegerField(null=True, blank=True, default=None)
    run_time = models.DateTimeField(null=True, blank=True, default=None)
    
    objects = managers.SnapshotManager()
    
    class Meta:
        db_table = 'snapshots'
        index_together = (
            ('txn',),
            ('collector_run',),
            ('parent_txn',),
            ('txn', 'collector_run'),
            ('statistic_id', 'collector_run'),
            ('run_time', 'collector_run'),
        )

# Access to the "TABLES" table from information_schema database        
class Tables(models.Model):
    table_catalog = models.CharField(db_column='TABLE_CATALOG', max_length=512)
    table_schema = models.CharField(db_column='TABLE_SCHEMA', max_length=64)
    table_name = models.CharField(db_column='TABLE_NAME', max_length=64, primary_key=True)
    table_type = models.CharField(db_column='TABLE_TYPE', max_length=64) 
    engine = models.CharField(db_column='ENGINE', max_length=64, blank=True) 
    version = models.BigIntegerField(db_column='VERSION', blank=True, null=True) 
    row_format = models.CharField(db_column='ROW_FORMAT', max_length=10, blank=True) 
    table_rows = models.BigIntegerField(db_column='TABLE_ROWS', blank=True, null=True) 
    avg_row_length = models.BigIntegerField(db_column='AVG_ROW_LENGTH', blank=True, null=True) 
    data_length = models.BigIntegerField(db_column='DATA_LENGTH', blank=True, null=True) 
    max_data_length = models.BigIntegerField(db_column='MAX_DATA_LENGTH', blank=True, null=True) 
    index_length = models.BigIntegerField(db_column='INDEX_LENGTH', blank=True, null=True) 
    data_free = models.BigIntegerField(db_column='DATA_FREE', blank=True, null=True) 
    auto_increment = models.BigIntegerField(db_column='AUTO_INCREMENT', blank=True, null=True) 
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True) 
    update_time = models.DateTimeField(db_column='UPDATE_TIME', blank=True, null=True) 
    check_time = models.DateTimeField(db_column='CHECK_TIME', blank=True, null=True) 
    table_collation = models.CharField(db_column='TABLE_COLLATION', max_length=32, blank=True) 
    checksum = models.BigIntegerField(db_column='CHECKSUM', blank=True, null=True) 
    create_options = models.CharField(db_column='CREATE_OPTIONS', max_length=255, blank=True) 
    table_comment = models.CharField(db_column='TABLE_COMMENT', max_length=2048)
    
    objects = managers.TableManager() 
    host = ''
    
    class Meta:
        managed = False
        db_table = 'TABLES'
        unique_together = (
            ('table_schema', 'table_name',),
        )
    
    def __unicode__(self):
        return u'%s.%s' % (self.table_schema, self.table_name)
        
    @property
    def create_syntax(self):
        k = get_db_key(self.host)
        if k is not None:
            cur = connections[k].cursor()
            cur.execute("SHOW CREATE TABLE `%s`.`%s`" % (self.table_schema, self.table_name))
            res = cur.fetchone()
            return res[1]
                
    @property
    def system_table(self):
        return self.table_type ==  "SYSTEM VIEW" or (
                                                        self.create_options is not None and
                                                        re.search('partitioned', self.create_options) and
                                                        self.create_time is None and
                                                        self.update_time is None
                                                    )

