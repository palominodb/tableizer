import re
import shutil
import sys
import traceback
from datetime import datetime, timedelta
from optparse import make_option, OptionError, OptionParser

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import humanize
import yaml

from ttt.collector import CollectorRegistry
from ttt.db import Db
from ttt.models import CollectorRun, Server, DatabaseTable, Snapshot
from utilities.utils import flatten

class BaseAction:
    def __init__(self, config, debug, *args):
        self.config = config
        self.debug = debug
        self.args = list(flatten(args))
        Db.open(self.config)
        
class PurgeAction(BaseAction):

    def execute(self):
        if len(self.args) < 1:
            print "Need at least one host to purge (try --help)."
            return 1
            
        if self.debug:
            print "Performing purge of %s" % (','.join(self.args))
            
        with transaction.commit_on_success():
            for host in self.args:
                if self.debug:
                    print "Doing purge for %s" % (host)
                    
                ### Clean out the references in the server tables
                s = Server.objects.find_by_name(host)
                schs = s.serverschema_set.all()
                tbls = DatabaseTable.objects.filter(schema__id__in=[x.id for x in schs])
                n = tbls.count()
                tbls.delete()
                if self.debug:
                    print "Deleted %d tables from the cache.." % (n)
                n = schs.count()
                schs.delete()
                if self.debug:
                    print "Deleted %d schemas from the cache.." % (n)
                s.delete()
                
                for col in CollectorRegistry.all():
                    items = col.stat.objects.filter(server=host)
                    n = items.count()
                    items.delete()
                    if self.debug:
                        print "Deleted %d records from %s table.." % (n, col.id)
                    cr_id = CollectorRun.objects.get_or_create(collector=col.id)[0].id
                    stat_ids = col.stat.objects.all().values_list('id', flat=True)
                    items = Snapshot.objects.filter(collector_run_id=cr_id).exclude(statistic_id__in=col.stat.objects.all().values_list('id', flat=True))
                    n = items.count()
                    items.delete()
                    if self.debug:
                        print "Deleted %d %s records from the snapshots table.." % (n, col.id)
        return 0
        
class RenameAction(BaseAction):

    def execute(self):
        if len(self.args) < 2:
            print 'Need host to rename and the newname for it (try --help).'
            return 1
            
        host = self.args.pop(0)
        newhost = self.args.pop(0)
        with transaction.commit_on_success():
            s = Server.objects.find_by_name(host)
            s.name = newhost
            s.save()
            for col in CollectorRegistry.all():
                n = col.stat.objects.filter(server=host).update(server=newhost)
                print 'Updated %d records in the %s table..' % (n, col.id)
        return 0
        
class ListAction(BaseAction):
    
    def execute(self):
        order_by = 'name'
        if len(self.args) == 1:
            k,v = self.args.pop(0).split('=')
            if k == 'order':
                order_by=v
            else:
                print 'Unknown options: %s for \'list\'' % (k)
        srvs = Server.objects.all().order_by(order_by)
        max_name = max(map(lambda x: len(x.name), srvs))
        max_size = max(map(lambda x: len(humanize.naturalsize(x.cached_size, binary=True) if x.cached_size is not None else ''), srvs))
        print '{2:^{0}} {3:^{1}} {4:^21}'.format(max_name, max_size+4, 'Host', 'Size', 'Last Updated')
        print '='*(max_name+max_size+4+21)
        for srv in srvs:
            print '{2:^{0}} {3:^{1}} {4}'.format(max_name, max_size+4, srv.name[:max_name],
                                                humanize.naturalsize(srv.cached_size, binary=True) if srv.cached_size is not None else '',
                                                srv.updated_at)
        return 0
        
#        max_name = srvs.map { |s| s.name.length }.max
#    max_size = sprintf("%4.3G", srvs.map { |s| s.cached_size / 1.0.gigabyte }.max).length
#    puts rf.format(
#      "Host#{" "*max_name}Size#{" "*(max_size+4)}Last Updated\n" +
#      "----#{"-"*max_name}----#{"-"*(max_size+4)}------------------------------",
#      ("["*max_name) + "   ]]]].[[[G" + "    ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]",
#      (srvs.map { |s| s.name }), (srvs.map { |s| s.cached_size / 1.0.gigabyte }),
#      (srvs.map { |s| s.updated_at })
#    )
        
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            '--config',
            dest='config',
            default=None,
            help='Path to ttt config file.',
        ),
        make_option(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Make the tool VERY noisy.',
        ),
        make_option(
            '--backup',
            action='store_true',
            dest='backup',
            default=False,
            help='Make an SQL dump that can be used to undo any changes made.'
        )
    )

    def handle(self, *args, **options):
        args = list(args)
        CollectorRegistry.load()
        
        for option in self.option_list:
            if option.dest == 'config':
                config_option = option
        if options.get('config') is None:
            raise OptionError('config parameter is required.', config_option)
        
        config = yaml.load(open(options.get('config'), 'r'))
        
        if len(args) < 1:
            print "Need an action (try --help)."
            sys.exit(1)
            
        if options.get('backup'):
            if config.get('ttt_connection', {}).get('adapter', '') != 'sqlite':
                print 'Can only backup sqlite3 TTT dbs.'
                sys.exit(1)
            if options.get('debug'):
                print 'Backing up TTT db..'
            shutil.copyfile(config.get('ttt_connection', {}).get('database', ''),
                            config.get('ttt_connection', {}).get('database', '') + '.bak')
                            
        action = args.pop(0)
        if action == 'purge':
            action = PurgeAction(config, options.get('debug', False), args)
        elif action == 'rename':
            action = RenameAction(config, options.get('debug', False), args)
        elif action == 'list':
            action = ListAction(config, options.get('debug', False), args)
        else:
            print 'Unknown action (try --help).'
            sys.exit(1)
          
        try:
            ecode = action.execute()
        except Exception, e:
            tb = traceback.format_exc()
            print tb
            sys.exit(1)
        sys.exit(ecode)