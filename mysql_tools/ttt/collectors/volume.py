from ttt.collector import Collector
from ttt.formatter import Formatter
from ttt.models import TableVolume, Server

def action(rd):
    import re
    srv = Server.objects.find_by_name(rd.host)
    srv.cached_size = 0
    dbs = {}
    rd.snapshot.clear()
    for t in rd.tables:
        if t.system_table:
            continue
        if t.table_schema not in dbs.keys():
            dbs[t.table_schema] = srv.serverschema_set.find_by_name(t.table_schema)
            dbs[t.table_schema].cached_size=0
        data_free = None
        tc = re.search('InnoDB free: (\d+)', t.table_comment)
        if tc:
            data_free = long(tc.groups()[0])*1024
        else:
            data_free = t.data_free
        tv = rd.stat(
            server=rd.host,
            database_name=t.table_schema,
            table_name=t.table_name,
            run_time=rd.run_time,
            data_length=t.data_length,
            data_free=data_free,
            index_length=t.index_length,
        )
        tv.save()
        rd.add(tv.id)
        rd.logger.info(
                "[volume] server:%s schema:%s table:%s data_length:%s index_length:%s" \
                % (rd.host, t.table_schema, t.table_name, str(t.data_length), str(t.index_length))
        )
        srv.cached_size += tv.size if tv.size is not None else 0
        dbs[tv.database_name].cached_size += tv.size if tv.size is not None else 0
    srv.save()
    for d in dbs.values():
        d.save()
        
    for t in rd.get_prev_version():
        rd.logger.info("[delete-check] %s.%s" % (t.database_name, t.table_name))
        g = rd.tables.find_by_schema_and_table(rd.host, t.database_name, t.table_name)
        if g is None and not rd.stat.objects.deleted(t):
            tbl = rd.stat(
                server=rd.host,
                database_name=t.table_schema,
                table_name=t.table_name,
                run_time=rd.run_time,
                data_length=None,
                data_free=None,
                index_length=None,
            )
            tbl.save()
            rd.add(tbl.id)
            rd.logger.info("[deleted] %s" % (rd.stat.objects.filter(id=t.id).values()))
            
    return rd

Collector(TableVolume, "table, index, and free size tracking", action)

def for_action(stream, data, options):
    display_width = options.get('display_width', 80)
    col_width = display_width/6 if options.get('full', False) else display_width/5
    server = str(data.server) if data.server is not None else ''
    database_name = str(data.database_name) if data.database_name is not None else ''
    table_name = str(data.table_name) if data.table_name is not None else ''
    if not options.get('header', False):
        if options.get('full', False):
            stream.write('{1:10} {2:{0}} {3:{0}} {4:{0}} {5:^18} {6:^18} {7:^18}\n'.format(col_width,
                                                                                        data.status[:10],
                                                                                        server[:col_width],
                                                                                        database_name[:col_width],
                                                                                        table_name[:col_width],
                                                                                        data.data_length/1024/1024 if data.data_length is not None else '',
                                                                                        data.index_length/1024/1024 if data.index_length is not None else '',
                                                                                        data.data_free/1024/1024 if data.data_free is not None else ''))
        else:
            stream.write('{1:10} {2:{0}} {3:{0}} {4:{0}} {5:^18}\n'.format(col_width,
                                                                        data.status[:10],
                                                                        server[:col_width],
                                                                        database_name[:col_width],
                                                                        table_name[:col_width],
                                                                        (data.data_length + data.index_length)/1024/1024 \
                                                                        if data.data_length is not None and data.index_length is not None else ''))
    else:
        if options.get('full', False):
            stream.write('{1:^10} {2:^{0}} {3:^{0}} {4:^{0}} {5:^18} {6:^18} {7:^18}\n'.format(col_width,
                                                                                        'status',
                                                                                        'server',
                                                                                        'database name',
                                                                                        'table name', 
                                                                                        'data length(mb)',
                                                                                        'index length(mb)',
                                                                                        'data free(mb)'))
        else:
            stream.write('{1:^10} {2:^{0}} {3:^{0}} {4:^{0}} {5:^18}\n'.format(col_width,
                                                                        'status',
                                                                        'server',
                                                                        'database name',
                                                                        'table name',
                                                                        'size(mb)'))

Formatter.proc_for('volume', 'text', for_action)
