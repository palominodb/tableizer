from ttt.collector import Collector
from ttt.formatter import Formatter
from ttt.models import TableView

def action(rd):
    for t in rd.tables:
        if t.table_type != 'VIEW':
            continue
        newt = rd.stat(
            server=rd.host,
            database_name=t.table_schema,
            table_name=t.table_name,
            create_syntax=t.create_syntax,
            run_time=rd.run_time,
        )
        oldt = rd.stat.objects.find_last_by_table(rd.host, t)
        if oldt is None or oldt.create_syntax is None:
            newt.save()
            rd.add(newt.id)
            rd.logger.info("[new] %s" % (rd.stat.objects.filter(id=newt.id).values()))
        elif newt.create_syntax != oldt.create_syntax:
            newt.save()
            rd.stat_updated(newt.id, oldt.id)
            rd.logger.info("[changed] %s" % (rd.stat.objects.filter(id=oldt.id).values()))
            
    for t in rd.get_prev_version():
        rd.logger.info("[delete-check] %s.%s" % (t.database_name, t.table_name))
        g = rd.tables.find_by_schema_and_table(t.database_name, t.table_name)
        if g is None and not rd.stat.objects.deleted(t):
            tbl = rd.stat(
                server=rd.host,
                database_name=t.table_schema,
                table_name=t.table_name,
                create_syntax=None,
                run_time=rd.run_time,
            )
            tbl.save()
            rd.stat_updated(tbl.id, t.id)
            rd.logger.info("[deleted] %s" % (rd.stat.objects.filter(id=t.id).values()))
            
    return rd
    
Collector(TableView,  "'create view' tracking", action)

def for_action(stream, data, options):
    display_width = options.get('display_width', 80)
    col_width = display_width/5
    if not options.get('header', False):
        stream.write('{1:^10} {2:^{0}} {3:^{0}} {4:^{0}} {5:^15}\n'.format(col_width,
                                                                            data.status,
                                                                            data.server[:col_width],
                                                                            data.database_name[:col_width],
                                                                            data.table_name[:col_width],
                                                                            str(data.created_at)))
        if options.get('full', False):
            stream.write('{1}\n{2:{0}}\n{3:{0}}\n{4}\n'.format(display_width,
                                                    'OLD:',
                                                    data.previous_version.create_syntax if data.previous_version is not None else '',
                                                    'NEW:',
                                                    data.create_syntax))
    else:
        stream.write('{1:^10} {2:^{0}} {3:^{0}} {4:^{0}} {5:^15}\n'.format(col_width, 'status', 'server', 'database name', 'table name', 'created at'))

Formatter.proc_for('view', 'text', for_action)
