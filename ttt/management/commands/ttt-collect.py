import logging
import sys
import traceback
from datetime import datetime
from optparse import make_option, OptionError

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import yaml
import MySQLdb

from pdb_dsn import dsn
from ttt.collector import CollectionDirector, CollectorRegistry
from ttt.db import Db
from ttt.models import Snapshot

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
            '-d',
            '--dsn',
            dest='dsn',
            default=None,
            help='Path to PalominoDB dsn.yml',
        ),
        make_option(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Make the tool VERY noisy.',
        ),
        make_option(
            '--stat',
            dest='stat',
            default=None,
            help='Collect a single <statistic>. See --list-stats for available statistics.'
        ),
        make_option(
            '--list-stats',
            action='store_true',
            dest='list_stats',
            default=False,
            help='List available statistics.'
        ),
    )

    def handle(self, *args, **options):
        CollectorRegistry.load()
        if options.get('list_stats'):
            cols = CollectorRegistry.all()
            print 'Available Statistics:'
            for col in cols:
               print "{0:20} - {1}".format(col.stat.collector, col.desc)
            sys.exit(0)
        
        for option in self.option_list:
            if option.dest == 'config':
                config_option = option
            elif option.dest == 'dsn':
                dsn_option = option
        if options.get('config') is None:
            raise OptionError('config parameter is required.', config_option)
        if options.get('dsn') is None:
            raise OptionError('dsn parameter is required.', dsn_option)
        
        Db.open(yaml.load(open(options.get('config'), 'r')))
        Db.migrate()
        dsn_schema = dsn.DSN(uri=options.get('dsn'))
        dsn_schema.validate()
        stats = options.get('stat')
        run_time = datetime.now()
        cur_col = None
        director = None
        
        if options.get('debug'):
            logger = logging.getLogger('django.db.backends')
            logger.setLevel(logging.DEBUG)
        
        try:
            with transaction.commit_on_success():
                hosts = filter(lambda x: dsn_schema.host_active(x) and dsn_schema.server_ttt(x), 
                                dsn_schema.get_all_hosts())
                txn_id = Snapshot.objects.get_next_txn()
                director = CollectionDirector(Db.app_config, run_time)
                rds = {}
                for host in hosts:
                    for coller in CollectorRegistry.all():
                        if stats is None or stats in coller.stat.collector:
                            cur_col = coller
                            rd = director.collect(host, coller)
                            if rds.get(rd.stat) is None:
                                rds[rd.stat] = []
                                print "NEW TXN: %d" % (txn_id)
                                print "rd changed: %s" % (rd.changed)
                                rds[rd.stat].append(rd)
                for k,v in rds.items():
                    changed = False
                    for i in v:
                        if i.changed:
                            changed = True
                            
                    if changed:
                        for i in v:
                            i.save(txn_id)
        except Exception, e:
            tb = traceback.format_exc()
            print tb
