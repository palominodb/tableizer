import glob
import logging
import os
import re
from datetime import datetime

from django.conf import settings
from django.db import connection, transaction, OperationalError, InternalError

from .models import CollectorRun, DatabaseTable, Server, ServerSchema, Snapshot, \
                    Tables
from utilities.utils import get_db_key

logger = logging.getLogger('django.db.backends')

class CollectorRunningError(Exception):
    pass

class CollectorRegistry(object):
    collectors = set()
    loaded = False
    
    @classmethod
    def all(cls):
        return list(cls.collectors)
    
    @classmethod
    def add(cls, o):
        cls.register(o)
    
    @classmethod
    def register(cls, obj):
        cls.collectors.add(obj)
        return list(cls.collectors)
    
    # Forces a reload of all the collectors.
    # Useful for a long-running application (such as a web interface)
    @classmethod
    def reload(cls):
        cls.unload()
        cls.load()
    
    # Loads all collectors    
    @classmethod
    def load(cls, from_path=os.path.join(os.path.dirname(__file__), 'collectors', '*')):
        if not cls.loaded:
            map(execfile, glob.glob(from_path+'.py'))
            cls.loaded = True
    
    # Forget all loaded collectors
    @classmethod
    def unload(cls):
        cls.collectors = set()
        cls.loaded = False

class CollectionDirector(object):
    
    class RunData(object):
        
        def __init__(self, host, tables, collector, run_time):
            self.host = host
            self.collector = collector
            self.tables = tables
            self.prev_snapshot = set(collector.stat.objects.find_most_recent_versions(collector.stat, extra_params={'server': host}, txn='latest').values_list('id', flat=True))
            self.cur_snapshot = self.prev_snapshot.copy()
            self.runref = CollectorRun.objects.get_or_create(collector=collector.id)[0]
            self.runref.last_run = run_time
            self.logger = logging.getLogger('django.db.backends')
        
        @property
        def this(self):
            return self.collector
        
        @property
        def stat(self):
            return self.collector.stat
        
        @property
        def run_time(self):
            return self.runref.last_run
        
        @property    
        def changed(self):
            return self.prev_snapshot != self.cur_snapshot
        
        @property
        def snapshot(self):
            return self.cur_snapshot
        
        def get_prev_version(self):
            return self.stat.objects.filter(id__in=self.prev_snapshot)
        
        def add(self, ids):
            self.cur_snapshot.add(ids)
        
        def stat_updated(self, new_id, old_id):
            self.add((new_id, old_id))
            self.delete(old_id)
        
        def delete(self, _id):
            try:
                self.cur_snapshot.remove(_id)
            except KeyError:
                pass
    
        def save(self, txn):
            self.runref.save()
            self.__save_run_ids(txn)
        
        def __save_run_ids(self, txn):
            for i in self.cur_snapshot:
                snap = Snapshot(txn=txn, collector_run=self.runref,
                                run_time=self.runref.last_run)
                if isinstance(i, list) or isinstance(i, tuple) or isinstance(i, set):
                    snap.statistic_id = i[0]
                    p_txn = Snapshot.objects.find_last_by_statistic_id(i[1])
                    if p_txn is not None:
                        snap.parent_txn = p_txn.id
                else:
                    snap.statistic_id = i
                snap.save()
    
    def __init__(self, run_time):
        self.host = None
        self.run_time = run_time
        self.cached_tables = None
        CollectorRegistry.load() # Make sure collectors are loaded.
            
    def recache_tables(self, collector):
        host = self.host
        k = get_db_key(host)
        if k is not None:
            tbls = Tables.objects.using(k).all()
            try:
                if settings.USE_INCLUDE_NOT_IGNORE:
                    report_include = settings.REPORT_INCLUDE
                    return_tbls = Tables.objects.using(k).none()
                    for tbl in tbls:
                        server_schema_table = '.'.join([host if host is not None else '', tbl.table_schema if tbl.table_schema is not None else '', 
                                            tbl.table_name if tbl.table_name is not None else ''])
                        do_inc = False
                        if report_include.get(collector.stat) is not None:
                            for reg in report_include.get(collector.stat, []):
                                re_match = re.match(reg, server_schema_table)
                                if re_match is not None:
                                    do_inc = True
                                    break
                        if not do_inc:
                            if report_include.get('global') is not None:
                                for reg in report_include.get('global', []):
                                    re_match = re.match(reg, server_schema_table)
                                    if re_match is not None:
                                        do_inc = True
                                        break
                        if do_inc:
                            return_tbls = return_tbls | tbls.filter(table_schema=tbl.table_schema,
                                                                    table_name=tbl.table_name)
                        else:
                            logger.info("[exclude tables]: %s" % (server_schema_table))
                    self.cached_tables = return_tbls
                else:
                    report_ignore = settings.REPORT_IGNORE
                    return_tbls = Tables.objects.using(k).none()
                    for tbl in tbls:
                        server_schema_table = '.'.join([host if host is not None else '', tbl.table_schema if tbl.table_schema is not None else '', 
                                            tbl.table_name if tbl.table_name is not None else ''])
                        do_rej = False
                        if report_ignore.get(collector.stat) is not None:
                            for reg in report_ignore.get(collector.stat, []):
                                re_match = re.match(reg, server_schema_table)
                                if re_match is not None:
                                    do_rej = True
                                    break
                        if not do_rej:
                            if report_ignore.get('global') is not None:
                                for reg in report_ignore.get('global', []):
                                    re_match = re.match(reg, server_schema_table)
                                    if re_match is not None:
                                        do_rej = True
                                        break
                        if not do_rej:
                            return_tbls = return_tbls | tbls.filter(table_schema=tbl.table_schema,
                                                                    table_name=tbl.table_name)
                        else:
                            logger.info("[exclude tables]: %s" % (server_schema_table))
                        self.cached_tables = return_tbls
            except Exception, e:
                print e
                self.cached_tables = tbls
      
    def collect(self, host, collector):
        with transaction.commit_on_success():
            rd = None
            if self.host != host:
                self.host = host
                try:
                    logger.info("[cache tables]: %s - %s" % (host, collector.stat))
                    self.recache_tables(collector)
                    
                    srv = Server.objects.get_or_create(name=host)[0]
                    srv.save()
                    for tbl in self.cached_tables:
                        sch = ServerSchema.objects.get_or_create(server=srv, name=tbl.table_schema)[0]
                        sch.save()
                        t = DatabaseTable.objects.get_or_create(schema=sch, name=tbl.table_name)[0]
                        t.save()
                except (OperationalError, InternalError):
                    prev = collector.stat.objects.find_last_by_server(host)
                    rd = CollectionDirector.RunData(host, None, collector, self.run_time)
                    if prev is None or prev.__class__.objects.unreachable(prev):
                        rd.logger.info("[unreachable]: %s - %s" % (host, rd.stat))
                    self.host = None
                except Exception:
                    raise
                    
            if rd is None:
                if settings.DATABASES.get('default', {}).get('ENGINE') == 'django.db.backends.mysql':
                    cur = connection.cursor()
                    cur.execute("SELECT GET_LOCK('ttt.collector.%s', 0.25)" % (collector.id))
                    if cur.fetchone()[0] != 1:
                        raise CollectorRunningError, "Only one collector per statistic may run at a time."
                        
                rd= CollectionDirector.RunData(self.host, self.cached_tables, collector, self.run_time)
                collector.run(rd)
                        
                if settings.DATABASES.get('default', {}).get('ENGINE') == 'django.db.backends.mysql':
                    cur = connection.cursor()
                    cur.execute("SELECT RELEASE_LOCK('ttt.collector.%s')" % (collector.id))
            
            return rd
                            
class Collector(object):

    def __init__(self, stat, desc, action):
        self.stat = stat
        self.desc = desc
        self.action = action
        CollectorRegistry.collectors.add(self)
        
    def __hash__(self):
        return hash((self.stat, self.desc))
        
    def __repr__(self):
        return "%s %s" % (self.stat,self.desc)
    
    def __eq__(self, other):
        return self.stat == other.stat
    
    @property    
    def id(self):
        return self.stat.collector
        
    def run(self, c_runner):
      c_runner.logger.info("[host-start] %s - %s" % (c_runner.host, c_runner.stat))
      res = self.action(c_runner)
      c_runner.logger.info("[host-end] %s - %s" % (c_runner.host, c_runner.stat))
      return res
