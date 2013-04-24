# managers.py
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
import time
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet

from utilities.utils import get_db_key

# Tables Manager
class TableMixin(object):
    
    def find_by_schema_and_table(self, host, database_name, table_name):
        k = get_db_key(host)
        if k is not None:
            tables = self.using(k).filter(table_schema=database_name, table_name=table_name)
            if tables.count() > 0:
                return tables[0]
            else:
                return None

class TableQuerySet(QuerySet, TableMixin):
    pass

class TableManager(models.Manager, TableMixin):
    
    def get_query_set(self):
        return TableQuerySet(self.model, using=self._db)

# Server Manager
class ServerMixin(object):
    
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
    
    def find_by_name(self, name):
        servers = self.filter(name=name)
        if servers.count() > 0:
            return servers[0]
        else:
            return None
            
class ServerQuerySet(QuerySet, ServerMixin):
    pass
            
class ServerManager(models.Manager, ServerMixin):
    
    def get_query_set(self):
        return ServerQuerySet(self.model, using=self._db)
        
# ServerSchema Manager
class ServerSchemaMixin(object):
    
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
    
    def find_by_name(self, name):
        schemas = self.filter(name=name)
        if schemas.count() > 0:
            return schemas[0]
        else:
            return None
            
class ServerSchemaQuerySet(QuerySet, ServerSchemaMixin):
    pass
            
class ServerSchemaManager(models.Manager, ServerSchemaMixin):
    
    def get_query_set(self):
        return ServerSchemaQuerySet(self.model, using=self._db)
        
# DatabaseTable Manager
class DatabaseTableMixin(object):

    def find_by_name(self, name):
        tables = self.filter(name=name)
        if tables.count() > 0:
            return tables[0]
        else:
            return None
            
class DatabaseTableQuerySet(QuerySet, DatabaseTableMixin):
    pass
    
class DatabaseTableManager(models.Manager, DatabaseTableMixin):

    def get_query_set(self):
        return DatabaseTableQuerySet(self.model, using=self._db)

# Snapshot Manager
class SnapshotMixin(object):

    def find_last_by_statistic_id(self, id_):
        snaps = self.filter(statistic_id=id_)
        if snaps.count() > 0:
            return snaps.order_by('-id')[0]
        else:
            return None

class SnapshotQuerySet(QuerySet, SnapshotMixin):
    pass
    
class SnapshotManager(models.Manager, SnapshotMixin):
    
    def get_query_set(self):
        return SnapshotQuerySet(self.model, using=self._db)
    
    def head(self, collector=None):
        head = self.all().aggregate(models.Max('txn'))
        head['txn__max'] = 0 if head['txn__max'] is None else head['txn__max']
        return head.get('txn__max')
    
    def get_next_txn(self):
        return self.head() + 1
        
    def stat_is_new(self, stat_obj):
        return self.filter(collector_run__id=stat_obj.collector_id, statistic_id=stat_obj.id).count() == 1
        
# TrackingTable Manager
class TrackingTableMixin(object):
    tables = {}
    c_id = None # cached collector id
    
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
    
    def find_most_recent_versions(self, cls, extra_params={}, txn=None):
        res = self.all()
        CollectorRun = models.get_model('ttt', 'CollectorRun')
        Snapshot = models.get_model('ttt', 'Snapshot')
        if TrackingTableManager.c_id is None:
            TrackingTableManager.c_id = CollectorRun.objects.get_or_create(collector=cls.collector)[0].id
        latest_txn = None
        try:
            latest_txn = Snapshot.objects.filter(collector_run__id=TrackingTableManager.c_id).order_by('-txn')[0].txn
        except Exception:
            latest_txn = Snapshot.objects.head()
        
        if isinstance(txn, int) and txn < 0:
            txn = latest_txn
            txn = 0 if txn < 0 else txn
        elif isinstance(txn, int) and txn > latest_txn:
            txn = latest_txn
        elif txn == 'latest':
            txn = latest_txn
        
        extra_copy = extra_params.copy()
        
        if cls.collector == 'user':
            if 'server' in extra_copy.keys():
                host = extra_copy.pop('server')
                extra_copy['host'] = host
            if 'database_name' in extra_copy.keys():
                db = extra_copy.pop('database_name')
                extra_copy['db'] = db
        res = res.filter(**extra_copy)
        res = res.extra(
            tables = ['snapshots'],
            where = ['snapshots.collector_run_id=%s %s AND %s.id=snapshots.statistic_id' % (str(TrackingTableManager.c_id),
                                                                                            '' if txn is None else 'AND snapshots.txn=%s' % (str(txn)),
                                                                                            cls._meta.db_table)]
        )
        return res
    
    def find_last_by_server(self, host):
        tts = self.filter(server=host)
        if tts.count() > 0:
            return tts.order_by('-id')[0]
        else:
            return None
        
    def find_last_by_table(self, server, i_s_table):
        try:
            tts = self.filter(server=server, database_name=i_s_table.table_schema, table_name=i_s_table.table_name)
        except Exception:
            tts = self.filter(server=server, db=i_s_table.table_schema, table_name=i_s_table.table_name)
        if tts.count() > 0:
            return tts.order_by('-id')[0]
        else:
            return None
    
    def previous_version(self, instance):
        try:
            tts = self.filter(id__lt=instance.id, server=instance.server,
                                database_name=instance.database_name, table_name=instance.table_name)
        except Exception:
            tts = self.filter(id__lt=instance.id, host=instance.server,
                                db=instance.database_name, table_name=instance.table_name)
        if tts.count() > 0:
            return tts.order_by('-id')[0]
        else:
            return None
            
    def history(self, instance, since=datetime.fromtimestamp(time.mktime([0,0,0,0,0,0,0,0,0]))):
        try:
            return self.filter(id__lte=instance.id, run_time__gte=since, server=instance.server,
                                database_name=instance.database_name, table_name=instance.table_name)
        except Exception:
            return self.filter(id__lte=instance.id, run_time__gte=since, server=instance.server,
                                db=instance.database_name, table_name=instance.table_name)
    
    def runs(self, over=None):
        q = self.all().order_by('run_time')
        if over is not None:
            q = q.filter(run_time__gt=over)
        q = q.distinct().values_list('run_time', flat=True)
        return q
        
    def servers(self):
        Server = models.get_model('ttt', 'Server')
        return Server.objects.all().values_list('name', flat=True)
        
    def schemas(self, server='all'):
        ServerSchema = models.get_model('ttt', 'ServerSchema')
        if server != 'all':
            return ServerSchema.objects.filter(server__name=server)
        else:
            return ServerSchema.objects.all()
            
    def tables(self, server='all', schema='all'):
        Server = models.get_model('ttt', 'Server')
        DatabaseTable = models.get_model('ttt', 'DatabaseTable')
        if server != 'all' and schema != 'all':
            return DatabaseTable.objects.filter(schema__name=schema, schema__server__name=server)
        elif server != 'all' and schema == 'all':
            return DatabaseTable.objects.filter(schema__server__name=server)
        elif server == 'all' and schema != 'all':
            return DatabaseTable.objects.filter(schema__name=schema)
        else:
            return DatabaseTable.objects.all()
        
class TrackingTableQuerySet(QuerySet, TrackingTableMixin):
    pass

class TrackingTableManager(models.Manager, TrackingTableMixin):

    def get_query_set(self):
        return TrackingTableQuerySet(self.model, using=self._db)
        
    def create_unreachable_entry(self, host, run_time):
        raise NotImplementedError, "This is an abstract method."
    
    def unreachable(self, instance):
        raise NotImplementedError, "This is an abstract method."
    
    def deleted(self, instance):
        raise NotImplementedError, "This is an abstract method."
    
    def tchanged(self, instance):
        raise NotImplementedError, "This is an abstract method."    
    
    def new(self, instance):
        last = self.previous_version(instance)
        return self.history(instance).count() == 1 or (last is not None and self.deleted(instance))
    
    def status(self, instance):
        if self.unreachable(instance):
            return 'unreachable'
        elif self.deleted(instance):
            return 'deleted'
        elif self.new(instance):
            return 'new'
        elif self.tchanged(instance):
            return 'changed'
        else:
            return 'unchanged'
            
# TableDefinition Manager
class TableDefinitionMixin(object):
    pass
    
class TableDefinitionQuerySet(QuerySet, TableDefinitionMixin):
    pass

class TableDefinitionManager(TrackingTableManager, TableDefinitionMixin):

    def get_query_set(self):
        return TableDefinitionQuerySet(self.model, using=self._db)

    def create_unreachable_entry(self, host, run_time):
        self.create(
            server=host,
            database_name=None,
            table_name=None,
            create_syntax=None,
            run_time=run_time,
        )
        
    def unreachable(self, instance):
        return instance.database_name is None and instance.table_name is None \
            and instance.create_syntax is None
            
    def deleted(self, instance):
        return instance.create_syntax is None and instance.updated_at is None
    
    def tchanged(self, instance):
        last = self.previous_version(instance)
        return last is None or self.deleted(instance) or last.create_syntax != instance.create_syntax
        
# TableVolume Manager
class TableVolumeMixin(object):
    
    def server_sizes(self, server, time='latest'):
        TableVolume = models.get_model('ttt', 'TableVolume')
        r = None
        if time == 'latest':
            r = self.find_most_recent_versions(TableVolume, {'server': server}, 'latest')
        else:
            r = self.find_most_recent_versions(TableVolume, {'server': server}, 'latest')
            r = r.extra(where=['snapshots.run_time=\'%s\'' % (time)])
        
        if r.count() == 0:
            raise Exception, 'no rows returned'
        d_length = 0
        i_length = 0
        last = None
        for t in r:
            last = t
            if t.unreachable:
                continue
            d_length += t.data_length if t.data_length is not None else 0
            i_length += t.index_length if t.index_length is not None else 0
        v = TableVolume(server=server, data_length=None if d_length == 0 else d_length,
                        index_length=None if i_length == 0 else i_length,
                        run_time=None if last is None else last.run_time)
        return v
    
    def server_sizes0(self, server, time='latest'):
        s = self.server_sizes(server, time)
        if s.data_length is None:
            s.data_length = 0
        if s.index_length is None:
            s.index_length = 0
        return s
        
    def database_sizes(self, server, database, time='latest'):
        TableVolume = models.get_model('ttt', 'TableVolume')
        r = None
        if time == 'latest':
            r = self.find_most_recent_versions(TableVolume, {'server': server}, 'latest')
        else:
            r = self.find_most_recent_versions(TableVolume, {'server': server}, 'latest')
            r = r.extra(where=['snapshots.run_time=\'%s\'' % (time)])
            
        if r.count() == 0:
            raise Exception, 'no rows returned'
            
        d_length = 0
        i_length = 0
        last = None
        for t in r:
            last = t
            if t.database_name != database:
                continue
            if t.unreachable:
                continue
            d_length += t.data_length if t.data_length is not None else 0
            i_length += t.index_length if t.index_length is not None else 0
        v = TableVolume(server=server, database_name=database,
                        data_length=None if d_length == 0 else d_length,
                        index_length=None if i_length == 0 else i_length,
                        run_time=None if last is None else last.run_time)
        return v
    
    def database_sizes0(self, server, database, time='latest'):
        s = self.database_sizes(server, database, time)
        if s.data_length is None:
            s.data_length = 0
        if s.index_length is None:
            s.index_length = 0
        return s
    
class TableVolumeQuerySet(QuerySet, TableVolumeMixin):
    pass
    
class TableVolumeManager(TrackingTableManager, TableVolumeMixin):

    def get_query_set(self):
        return TableVolumeQuerySet(self.model, using=self._db)

    def create_unreachable_entry(self, host, run_time):
        self.create(
            server=host,
            database_name=None,
            table_name=None,
            data_free=None,
            index_length=None,
            data_length=None,
            run_time=run_time
        )
        
    def unreachable(self, instance):
        return instance.database_name is None and instance.table_name is None \
            and instance.data_length is None and instance.index_length is None \
            and instance.data_free is None
    
    def deleted(self, instance):
        return instance.data_length is None and instance.index_length is None \
            and instance.data_free is None

    def tchanged(self, instance):
        prev = self.previous_version(instance)
        if prev is None:
            return True
        else:
            return instance.data_length != prev.data_length or instance.index_length != prev.index_length
            
# TableView Manager
class TableViewMixin(object):
    pass
    
class TableViewQuerySet(QuerySet, TableViewMixin):
    pass
    
class TableViewManager(TrackingTableManager, TableViewMixin):

    def get_query_set(self):
        return TableViewQuerySet(self.model, using=self._db)
        
    def create_unreachable_entry(self, host, run_time):
        self.create(
            server=host,
            database_name=None,
            table_name=None,
            create_syntax=None,
            run_time=run_time,
        )
        
    def unreachable(self, instance):
        return instance.database_name is None and instance.table_name is None \
            and instance.create_syntax is None
            
    def deleted(self, instance):
        return instance.create_syntax is None
        
    def tchanged(self, instance):
        Snapshot = models.get_model('ttt', 'Snapshot')
        last=self.previous_version(instance)
        return (last is None and Snapshot.objects.stat_is_new(instance)) \
            or last is not None and (self.deleted(last) or last.create_syntax != instance.create_syntax)
            
# TableUser Manager
class TableUserMixin(object):
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
    
class TableUserQuerySet(QuerySet, TableUserMixin):
    pass
    
class TableUserManager(TrackingTableManager, TableUserMixin):

    def get_query_set(self):
        return TableUserQuerySet(self.model, using=self._db)
        
    def create_unreachable_entry(self, host, run_time):
        self.create(
            server=host,
            run_time=run_time,
            permtype=self.UNREACHABLE_ENTRY,
        )
         
    def unreachable(self, instance):
        return instance.permtype & instance.UNREACHABLE_ENTRY != 0
    
    def deleted(self, instance):
        return instance.permtype & instance.DELETED_PERMISSION != 0
    
    def tchanged(self, instance):
        last = self.previous_version(instance)
        return last is None or self.deleted(last) or instance.perms_set != last.perms_set
