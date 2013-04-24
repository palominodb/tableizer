# rrd.py
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

from ttt.formatter import Formatter

class RRDFormatter(Formatter):

    def lastupd_rrd(self, path):    
        import rrdtool
        import time
        from datetime import datetime
        try:
            return datetime.fromtimestamp(rrdtool.last(str(path)))
        except Exception:
            return datetime.fromtimestamp(time.mktime([1970,1,1,0,0,0,0,0,0]))
            
    def update_rrd(self, path, time_at, values):
        import rrdtool
        import time
        from utilities.utils import flatten
        time_at = int(time.mktime(time_at.timetuple()))
        vals = list(flatten([time_at, values]))
        vals = map(lambda x: str(x), vals)
        rrdtool.update(str(path), ':'.join(vals))
    
    def create_rrd(self, path, step, start):
        import os
        import rrdtool
        import time
        if not os.path.isfile(path):
            try:
                os.makedirs(os.path.split(path)[0])
            except Exception:
                pass
            rra_s = []
            for rra in ['AVERAGE', 'MAX', 'MIN']:
                for cyl in [[1, 172800.0], [2, 1209600.0], [4, 2592000.0], [8,  15552000.0], [16, 31557600.0], [32, 63115200.0]]:
                    incr = cyl[0]
                    wind = cyl[1]
                    if step < wind:
                        rra_s.append('RRA:%s:0.25:%s:%s' % (rra, str(incr), str(float(wind/step))))
            rrdtool.create(
                str(path), '--step', str(step), '--start', str(int(time.mktime(start.timetuple()))-1),
                'DS:data_length:GAUGE:%s:U:U' % (str(step*2)),
                'DS:index_length:GAUGE:%s:U:U' % (str(step*2)),
                'DS:data_free:GAUGE:%s:U:U' % (str(step*2)),
                rra_s,
            )
            
    def format(self, rows, *args):
        import os
        from datetime import timedelta
        from django.db.models import get_model
        TableVolume = get_model('ttt', 'TableVolume')
        CollectorRun = get_model('ttt', 'CollectorRun')
        Server = get_model('ttt', 'Server')
        stream = self.stream
        args = list(args)
        options = self.__extract_options__(args)
        path = self.need_option("path")
        updint = self.need_option("update_interval")
        regex = re.search('(\d+(?:\.?\d+)?)([hdwm])?', updint)
        
        if regex is not None:
            num, unit = regex.groups()
            num = float(num)
            if unit == 'm':
                updint = timedelta(minutes=num)
            elif unit == 'h':
                updint = timedelta(hours=num)
            elif unit == 'd':
                updint = timedelta(days=num)
            else:
                updint = timedelta()
        else:
            updint = timedelta()
        
        updint = int(updint.total_seconds())
        
        if updint == 0:
            raise Exception, 'Option update_interval must resolve to a number greater than 0.'
        
        last_run = CollectorRun.objects.get_or_create(collector='volume')[0].last_run
        runs = TableVolume.objects.runs()
        
        for srv in TableVolume.objects.servers():
            rrd_path = '%s/%s/server_%s.rrd' % (path, srv, srv)
            last = self.lastupd_rrd(rrd_path)
            if not os.path.isfile(rrd_path):
                self.create_rrd(rrd_path, updint, TableVolume.objects.filter(server=srv).order_by('id')[0].run_time)
            if last < last_run:
                max_run = Server.objects.find_by_name(srv).updated_at
                filtered_runs = filter(lambda r: r > last, runs)
                for run in filtered_runs:
                    if run > max_run:
                        continue
                    try:
                        s = TableVolume.objects.server_sizes0(srv, run)
                    except Exception, e:
                        continue
                    self.update_rrd(rrd_path, run, [s.data_length, s.index_length, 'U'])
                
        for sch in TableVolume.objects.schemas():
            if sch.name == 'information_schema':
                continue
            srv = sch.server.name
            rrd_path = '%s/%s/database_%s.rrd' % (path, srv, sch.name)
            last = self.lastupd_rrd(rrd_path)
            if not os.path.isfile(rrd_path):
                self.create_rrd(rrd_path, updint, TableVolume.objects.filter(server=srv, database_name=sch.name).order_by('id')[0].run_time)
            if last < last_run:
                max_run = sch.updated_at
                filtered_runs = filter(lambda r: r > last, runs)
                for run in filtered_runs:
                    if run > max_run:
                        continue
                    try:
                        s = TableVolume.objects.database_sizes0(srv, sch.name, run)
                    except Exception, e:
                        continue
                    self.update_rrd(rrd_path, run, [s.data_length, s.index_length, 'U'])
                    
        for tbl in TableVolume.objects.tables():
            srv = tbl.schema.server.name
            sch = tbl.schema.name
            if sch == 'information_schema':
                continue
            rrd_path = '%s/%s/%s/%s.rrd' % (path, srv, sch, tbl.name)
            last = self.lastupd_rrd(rrd_path)
            if not os.path.isfile(rrd_path):
                self.create_rrd(rrd_path, updint, TableVolume.objects.filter(server=srv, database_name=sch, table_name=tbl.name).order_by('id')[0].run_time)
            if last < last_run:
                max_run = tbl.updated_at
                filtered_runs = filter(lambda r: r > last, runs)
                for run in filtered_runs:
                    if run > max_run:
                        continue
                    try:
                        s = TableVolume.objects.filter(run_time=run, server=srv, database_name=sch, table_name=tbl.name).order_by('id')[0]
                    except Exception, e:
                        continue
                    if s.data_length is None:
                        s.data_length = 0
                    if s.index_length is None:
                        s.index_length = 0
                    if s.data_free is None:
                        s.data_free = 0
                    self.update_rrd(rrd_path, run, [s.data_length, s.index_length, s.data_free])          
        return 0

RRDFormatter.runner_for('rrd')
