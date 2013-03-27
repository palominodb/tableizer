import re
import sys
import traceback
from datetime import datetime, timedelta
from optparse import make_option, OptionError, OptionParser

from django.core.management.base import BaseCommand, CommandError

import yaml

from ttt.collector import CollectorRegistry
from ttt.db import Db
from ttt.formatter import Formatter
from ttt.models import TrackingTable

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
            '--stat',
            dest='stat',
            default='definition',
            help='Collect a single <statistic>. See --list-stats for available statistics.'
        ),
        make_option(
            '--list-stats',
            action='store_true',
            dest='list_stats',
            default=False,
            help='List available statistics.'
        ),
        make_option(
            '-o',
            '--output',
            dest='output',
            default='text',
            help='Specifies an output formatter. One of: email, text, nagios, rrd'
        ),
        make_option(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Make the tool VERY noisy.',
        ),
        make_option(
            '-s',
            '--since',
            dest='since',
            default='',
            help='Where <since> is something like: last(since the last collector run), 4h(4 hours), 1d(1 day), 1w(1 week)',
        ),
        make_option(
            '--raw',
            action='store_true',
            dest='output_raw',
            default=False,
            help='Disable \'ignore tables\' processing.',
        ),
        make_option(
            '--width',
            dest='output_width',
            default=None,
            help='Number of columns to format to.',
            type=int,
        ),
        make_option(
            '--full',
            action='store_true',
            dest='output_full',
            default=False,
            help='Full output',
        ),
        make_option(
            '--where',
            dest='where',
            default=None,
            help='Cannot presently be specified when \'last-collect\' is used with --since.',
        ),
        make_option(
            '--order',
            dest='order_by',
            default=None,
            help='Select columns to order by. Technically an SQL fragment. Same column list as above.',
        ),
        make_option(
            '--group',
            dest='group_by',
            default=None,
            help='(TODO) Comma separated list of columns to group by. Same columns as above.',
        ),
        make_option(
            '--select',
            dest='select_columns',
            default=None,
            help='(TODO) SQL fragment. Try running with debug to see your full query.',
        ),
        make_option(
            '--limit',
            dest='limit',
            default=None,
            help='Limit to N results.',
            type=int,
        ),
    )

    def handle(self, *args, **options):
        output_cfg = {}
        sql_conditions = {}
        find_type = 'normal'
    
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
        if options.get('config') is None:
            raise OptionError('config parameter is required.', config_option)
        
        Db.open(yaml.load(open(options.get('config'), 'r')))
        cfg = Db.app_config
        
        since_regex = re.search('(\d+(?:\.?\d+)?)([hdwm])?', options.get('since', ''))
        if options.get('since') == 'last':
            find_type = 'last'
        elif since_regex is not None:
            num, unit = since_regex.groups()
            num = float(num)
            if unit == 'h':
                time = datetime.now() - timedelta(hours=num)
            elif unit == 'd':
                time = datetime.now() - timedelta(days=num)
            elif unit == 'w':
                time = datetime.now() - timedelta(weeks=num)
            elif unit == 'm':
                time = datetime.now() - timedelta(minutes=num)
            else:
                time = datetime.now() - timedelta(seconds=num)
            sql_conditions['since'] = time
                
        if options.get('where') is not None:
            sql_conditions['where'] = options.get('where')
        
        if options.get('group_by') is not None:
            sql_conditions['group'] = options.get('group_by')
            
        if options.get('select_columns') is not None:
            sql_conditions['select'] = options.get('select_columns')
            
        if options.get('order_by') is not None:
            sql_conditions['order'] = options.get('order_by')
            
        if options.get('limit') is not None:
            sql_conditions['limit'] = options.get('limit')
        
        if 'report_options' in cfg.keys():
            for k,v in cfg.get('report_options', {}).items():
                output_cfg[k] = v
                
        output_cfg['full'] = options.get('output_full')
        output_cfg['raw'] = options.get('output_raw')
        
        output = Formatter.get_runner_for(options.get('output'))(sys.stderr, cfg)
        
        try:
            Model = TrackingTable._TrackingTable__tables.get(options.get('stat', 'definition'))
            if find_type == 'normal':
                query = Model.objects.all()
            else:
                query = Model.objects.find_most_recent_versions(Model)
            
            if sql_conditions.get('since') is not None:
                query = query.filter(run_time__gte=sql_conditions.get('since'))
            if sql_conditions.get('where') is not None:
                query = query.extra(where=[sql_conditions.get('where'),])
            if sql_conditions.get('order') is not None:
                cols = sql_conditions.get('order').split(',')
                query = query.order_by(*cols)
            if sql_conditions.get('limit') is not None:
                query = query[:sql_conditions.get('limit')]
            output.format(query, output_cfg)
        except Exception, e:
            tb = traceback.format_exc()
            print tb
