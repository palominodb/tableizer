# tableizer-query.py
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
import logging
import re
import sys
import traceback
from datetime import datetime, timedelta
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from ttt.collector import CollectorRegistry
from ttt.formatter import Formatter
from ttt.models import TrackingTable

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
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
        code = 0
    
        CollectorRegistry.load()
        if options.get('list_stats'):
            cols = CollectorRegistry.all()
            print 'Available Statistics:'
            for col in cols:
               print "{0:20} - {1}".format(col.stat.collector, col.desc)
            sys.exit(0)
            
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
        
        for k,v in settings.REPORT_OPTIONS.items():
            output_cfg[k] = v
                
        output_cfg['full'] = options.get('output_full')
        output_cfg['raw'] = options.get('output_raw')
        output_cfg['display_width'] = options.get('output_width')
        
        output = Formatter.get_runner_for(options.get('output'))(sys.stderr)
        
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
            
            # Do reject_ignores filter before limit
            if not output_cfg.get('raw', False):
                if settings.USE_INCLUDE_NOT_IGNORE:
                    query = output.report_include(query)
                else:
                    query = output.reject_ignores(query)
            if sql_conditions.get('limit') is not None:
                query = query[:sql_conditions.get('limit')]
            code = output.format(query, output_cfg)
        except Exception, e:
            tb = traceback.format_exc()
            if settings.SEND_CRASHREPORTS:
                logger = logging.getLogger('tableizer')
            else:
                logger = logging.getLogger('management_command')
            logger.error(tb)
        sys.exit(code)
