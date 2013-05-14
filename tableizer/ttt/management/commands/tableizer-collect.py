# tableizer-collect.py
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
import sys
import traceback
from datetime import datetime
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from ttt.collector import CollectionDirector, CollectorRegistry
from ttt.models import Snapshot

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
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
        
        stats = options.get('stat')
        run_time = datetime.now()
        cur_col = None
        director = None
        
        if options.get('debug'):
            logger = logging.getLogger('django.db.backends')
            logger.setLevel(logging.DEBUG)
        
        try:
            with transaction.commit_on_success():
                dbs = settings.TABLEIZER_DBS    #Get all db settings except for the default
                txn_id = Snapshot.objects.get_next_txn()
                director = CollectionDirector(run_time)
                rds = {}
                for k,v in dbs.items():
                    host = v.get('HOST') if v.get('HOST') is not None and v.get('HOST') != '' else 'localhost'
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
            if settings.SEND_CRASHREPORTS:
                logger = logging.getLogger('tableizer')
            else:
                logger = logging.getLogger('management_command')
            logger.error(tb)
