import os

from django.conf import settings

import rrdtool

from utilities.utils import flatten, titleize, str_to_datetime, datetime_to_int
    
class Rrdtool(object):

    def server_graph(self, servers, since, type_='full'):
        msgs = []
        ok = True
        for srv in flatten([servers]):
            path = settings.FORMATTER_OPTIONS.get('rrd', {}).get('path', '')
            rrd_path = os.path.join(path, srv.name, 'server_%s.rrd' % (srv.name))
            opts = self.__common_opts('server_%s' % (srv.name), since, type_, 'Server Aggregate - %s' % (srv.name))
            
            opts.append(map(lambda ds: self.__common_ds_opts(ds, rrd_path), [
                ['data_length', ['AREA%s:STACK', '#00ff40']],
                ['index_length', ['AREA%s', '#0040ff']],
                #['data_free', ['LINE2%s', '#0f00f0']],
            ]))
            
            opts = flatten(opts)
            opts = map(lambda x: str(x), opts)
            
            try:
                rrdtool.graph(opts)
            except Exception, e:
                msgs.append(e)
                ok = False
        return [ok, msgs]
            
    def database_graph(self, databases, since, type_='full'):
        msgs = []
        ok = True
        for db in flatten([databases]):
            path = settings.FORMATTER_OPTIONS.get('rrd', {}).get('path', '')
            rrd_path = os.path.join(path, db.server.name, 'database_%s.rrd' % (db.name))
            opts = self.__common_opts('database_%s_%s' % (db.server.name, db.name), since,
                                        type_, 'Database Aggregate - %s.%s' % (db.server.name, db.name))
            
            opts.append(map(lambda ds: self.__common_ds_opts(ds, rrd_path), [
                ['data_length', ['AREA%s:STACK', '#00ff40']],
                ['index_length', ['AREA%s', '#0040ff']],
                #['data_free', ['LINE2%s', '#0f00f0']],
            ]))
            
            opts = flatten(opts)
            opts = map(lambda x: str(x), opts)
            try:
                rrdtool.graph(opts)
            except Exception, e:
                msgs.append(e)
                ok = False
        return [ok, msgs]
            
    def table_graph(self, tables, since, type_='full'):
        msgs = []
        ok = True
        for tbl in flatten([tables]):
            path = settings.FORMATTER_OPTIONS.get('rrd', {}).get('path', '')
            rrd_path = os.path.join(path, tbl.schema.server.name, tbl.schema.name, '%s.rrd' % (tbl.name))
            opts = self.__common_opts('table_%s_%s_%s' % (tbl.schema.server.name, tbl.schema.name, tbl.name),
                                        since, type_, 'Table - %s.%s.%s' % (tbl.schema.server.name, tbl.schema.name, tbl.name))
                                        
            opts.append(map(lambda ds: self.__common_ds_opts(ds, rrd_path), [
                ['data_length', ['AREA%s:STACK', '#00ff40']],
                ['index_length', ['AREA%s', '#0040ff']],
                #['data_free', ['LINE2%s', '#0f00f0']],
            ]))
            
            opts = flatten(opts)
            opts = map(lambda x: str(x), opts)
            try:
                rrdtool.graph(opts)
            except Exception, e:
                msgs.append(e)
                ok = False
        return [ok, msgs]
    
    def __common_opts(self, path_frag, since, type_, title):
        filename = '%s.%s.%s.png' % (path_frag, since, type_)
        since = str_to_datetime(since)
        since = datetime_to_int(since)
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'graphs')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'graphs'))
        path = os.path.join(settings.MEDIA_ROOT, 'graphs', filename)
        o = [path, '-s', str(since), '--width', '640' if type_ == 'full' else '128',
            '-e', 'now', '--title', '%s' % (str(title))]
            
        if type_ == 'thumb':
            o.append('-j')
            o.append('--height')
            o.append('16')
        return o
        
    def __common_ds_opts(self, ds, rrd_path):
        dsname = ds[0]
        gitems = ds[1:]
        ret = []
        ret.append('DEF:avg_{0}={1}:{0}:AVERAGE'.format(dsname, rrd_path))
        ret.append('DEF:min_{0}={1}:{0}:MIN'.format(dsname, rrd_path))
        ret.append('DEF:max_{0}={1}:{0}:MAX'.format(dsname, rrd_path))
        ret.append('VDEF:v_last_{0}=avg_{0},LAST'.format(dsname))
        ret.append('VDEF:v_avg_{0}=avg_{0},AVERAGE'.format(dsname))
        ret.append('VDEF:v_min_{0}=avg_{0},MINIMUM'.format(dsname))
        ret.append('VDEF:v_max_{0}=avg_{0},MAXIMUM'.format(dsname))
        for gi in gitems:
            ret.append(gi[0] % ':avg_{0}{1}:"{2}"'.format(dsname, gi[1], titleize(dsname)))
        ret.append('GPRINT:v_last_{0}:"Current\\: %0.2lf%s"'.format(dsname))
        ret.append('GPRINT:v_avg_{0}:"Avg\\: %0.2lf%s"'.format(dsname))
        ret.append('GPRINT:v_min_{0}:"Min\\: %0.2lf%s"'.format(dsname))
        ret.append('GPRINT:v_max_{0}:"Max\\: %0.2lf%s"'.format(dsname))
        ret.append('COMMENT:"\\s"')
        ret.append('COMMENT:"\\s"')
        return ret
