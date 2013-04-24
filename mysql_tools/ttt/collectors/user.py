# user.py
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
from django.db import transaction

import MySQLdb

from ttt.collector import Collector
from ttt.formatter import Formatter
from ttt.models import TableUser

def action(rd):
    # Converts dictionary keys to lowercase
    def __dict_change_key_case(input, case='lower'):
        CASE_LOWER = 'lower'
        CASE_UPPER = 'upper'
        if case == CASE_LOWER:
            f = str.lower
        elif case == CASE_UPPER:
            f = str.upper
        else:
            raise ValueError()
        return dict((f(k), v) for k, v in input.items())

    from ttt.db import Db
    connection = Db.open_schema(rd.host, 'mysql')
    cursor = connection.cursor()
    query_template = "SELECT * FROM %s"
    cursor.execute(query_template % 'user')
    mysqlusers = cursor.fetchall()
    cursor.execute(query_template % 'host')
    mysqlhosts = cursor.fetchall()
    cursor.execute(query_template % 'db')
    mysqldbs = cursor.fetchall()
    cursor.execute(query_template % 'tables_priv')
    mysqltables = cursor.fetchall()
    cursor.execute(query_template % 'columns_priv')
    mysqlcolumns = cursor.fetchall()
    cursor.execute(query_template % 'procs_priv')
    mysqlprocs = cursor.fetchall()
    
    prev_version = rd.get_prev_version()
    
    # Global privileges
    for mu in mysqlusers:
        mu = __dict_change_key_case(mu)
        user = mu.get('user')
        host = mu.get('host')
        pus = list(prev_version.filter(user=user, host=host))
        pus = filter(lambda x: x.global_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
        mu.update({
            'server': rd.host,
            'created_at': rd.run_time,
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        s = rd.stat(**mu)
        s.permtype = rd.stat.GLOBAL_PERMISSION
        rd.logger.debug("[new global user priv]: '%s'@'%s'" % (s.user, s.host))
        s.save()
        rd.add(s.id)
        
    # Host level privs
    for mu in mysqlhosts:
        mu = __dict_change_key_case(mu)
        host = mu.get('host')
        db = mu.get('db')
        pus = list(prev_version.filter(host=host, db=db))
        pus = filter(lambda x: x.host_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
        mu.update({
            'server': rd.host,
            'created_at': rd.run_time,
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        s = rd.stat(**mu)
        s.permtype = rd.stat.HOST_PERMISSION
        rd.logger.debug("[new host user priv]: *.* from '%s'@'%s'" % (s.user, s.host))
        s.save()
        rd.add(s.id)
        
    # DB level privs
    for mu in mysqldbs:
        mu = __dict_change_key_case(mu)
        user = mu.get('user')
        host = mu.get('host')
        db = mu.get('db')
        pus = list(prev_version.filter(user=user, host=host, db=db))
        pus = filter(lambda x: x.db_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
        mu.update({
            'server': rd.host,
            'created_at': rd.run_time,
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        s = rd.stat(**mu)
        s.permtype = rd.stat.DB_PERMISSION
        rd.logger.debug("[new db user priv]: `%s`.* from '%s'@'%s'" % (s.db, s.user, s.host))
        s.save()
        rd.add(s.id)
      
    # Table level privs
    for mu in mysqltables:
        mu = __dict_change_key_case(mu)
        user = mu.get('user')
        host = mu.get('host')
        db = mu.get('db')
        table_name = mu.get('table_name')
        pus = list(prev_version.filter(user=user, host=host, db=db, table_name=table_name))
        pus = filter(lambda x: x.table_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
            
        mu.update({
            'server': rd.host,
            'created_at': mu.get('timestamp'),
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        mu.pop('timestamp')
        # Column_priv masks the various column level privileges that are applied to a table
        # MySQL uses it to determine if it should look in column_priv. We currently don't track this
        # since we're tracking column_priv table anyway.
        # And while tracking it could be used to sniff out corruption or perhaps privilege abuse
        # it doesn't seem worthwhile straight away.
        mu.pop('column_priv')
        tprivs = rd.stat.perms_from_setstr(mu.get('table_priv'))
        mu.pop('table_priv')
        s = rd.stat(**mu)
        s.perms_from_set(tprivs)
        s.permtype = rd.stat.TABLE_PERMISSION
        rd.logger.debug("[new table user priv]: `%s`.`%s` from '%s'@'%s'" % (s.db, s.table_name, s.user, s.host))
        s.save()
        rd.add(s.id)
        
    # Column level privs
    for mu in mysqlcolumns:
        mu = __dict_change_key_case(mu)
        user = mu.get('user')
        host = mu.get('host')
        db = mu.get('db')
        table_name = mu.get('table_name')
        column_name = mu.get('column_name')
        pus = list(prev_version.filter(user=user, host=host, db=db, table_name=table_name, column_name=column_name))
        pus = filter(lambda x: x.column_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
        
        mu.update({
            'server': rd.host,
            'created_at': mu.get('timestamp'),
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        tprivs = rd.stat.perms_from_setstr(mu.get('column_priv'))
        mu.pop('timestamp')
        mu.pop('column_priv')
        s = rd.stat(**mu)
        s.perms_from_set(tprivs)
        s.permtype = rd.stat.COLUMN_PERMISSION
        rd.logger.debug("[new column user priv]: `%s`.`%s`.`%s` from '%s'@'%s'" % (s.db, s.table_name, s.column_name, s.user, s.host))
        s.save()
        rd.add(s.id)
        
    # Proc level privs
    for mu in mysqlprocs:
        mu = __dict_change_key_case(mu)
        user = mu.get('user')
        host = mu.get('host')
        db = mu.get('db')
        routine_name = mu.get('routine_name')
        routine_type = mu.get('routine_type')
        pus = list(prev_version.filter(user=user, host=host, db=db, routine_name=routine_name, routine_type=routine_type))
        pus = filter(lambda x: x.proc_perm, pus)
        pu = pus[0] if len(pus) > 0 else None
        if pu is not None:
            continue
            
        mu.update({
            'server': rd.host,
            'created_at': mu.get('timestamp'),
            'updated_at': rd.run_time,
            'run_time': rd.run_time,
        })
        tprivs = rd.stat.perms_from_setstr(mu.get('proc_priv'))
        mu.pop('timestmap')
        mu.pop('proc_priv')
        s = rd.stat(**mu)
        s.perms_from_set(tprivs)
        s.permtype = rd.stat.PROC_PERMISSION
        rd.logger.debug("[new proc priv]: `%s`.`%s`.`%s` from '%s'@'%s'" % (s.db, s.table_name, s.column_name, s.user, s.host))
        s.save()
        rd.add(s.id)
    
    for u in prev_version:
        curp = None
        if u.permtype & ~0x3 == rd.stat.GLOBAL_PERMISSION:
            for mu in mysqlusers:
                mu = __dict_change_key_case(mu)
                user = mu.get('user')
                host = mu.get('host')
                if u.user == user and u.host == host:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.HOST_PERMISSION:
            for mu in mysqlhosts:
                mu = __dict_change_key_case(mu)
                host = mu.get('host')
                db = mu.get('db')
                if u.host == host and u.db == db:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.DB_PERMISSION:
            for mu in mysqldbs:
                mu = __dict_change_key_case(mu)
                host = mu.get('host')
                db = mu.get('db')
                user = mu.get('user')
                if u.host == host and u.db == db and u.user == user:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.TABLE_PERMISSION:
            for mu in mysqltables:
                mu = __dict_change_key_case(mu)
                host = mu.get('host')
                db = mu.get('db')
                user = mu.get('user')
                table_name = mu.get('table_name')
                if u.host == host and u.db == db and u.user == user and u.table_name == table_name:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.COLUMN_PERMISSION:
            for mu in mysqlcolumns:
                mu = __dict_change_key_case(mu)
                host = mu.get('host')
                db = mu.get('db')
                user = mu.get('user')
                table_name = mu.get('table_name')
                column_name = mu.get('column_name')
                if u.host == host and u.db == db and u.user and user and \
                        u.table_name == table_name and u.column_name == column_name:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.PROC_PERMISSION:
            for mu in mysqlprocs:
                mu = __dict_change_key_case(mu)
                host = mu.get('host')
                db = mu.get('db')
                user = mu.get('user')
                routine_name = mu.get('routine_name')
                routine_type = mu.get('routine_type')
                if u.host == host and u.db == db and u.user == user and \
                        u.routine_name == routine_name and u.routine_type == routine_type:
                    curp = mu
                    break
        elif u.permtype & ~0x3 == rd.stat.UNREACHABLE_ENTRY:
            continue
        else:
            raise RuntimeError, "Invalid, Corrupt, or hand modified data found. Found user was not of any known type."
            curp = None
        
        if rd.stat.objects.deleted(u) and curp is None:
            continue
        # Delete check
        if curp is None and not rd.stat.objects.deleted(u):
            u_dict = u.__dict__
            u_dict.update({
                'created_at': None,
                'updated_at': None,
                'run_time': rd.run_time,
                'permtype': u.permtype | rd.stat.DELETED_PERMISSION,
            })
            newu = rd.stat(**u_dict)
            newu.save()
            rd.stat_updated(newu.id, u.id)
            continue
            
        changed = False
        cols = [
            'password', 'grantor', 'ssl_type', 'ssl_cipher', 'x509_issuer', 'x509_subject',
            'max_questions', 'max_updates', 'max_connections', 'max_user_connections',
            'plugin', 'authentication_string', 'create_priv', 'drop_priv', 'grant_priv',
            'references_priv', 'event_priv', 'alter_priv', 'delete_priv', 'index_priv',
            'insert_priv', 'select_priv', 'update_priv', 'create_tmp_table_priv',
            'lock_tables_priv', 'trigger_priv', 'create_view_priv', 'show_view_priv',
            'execute_priv', 'file_priv', 'create_user_priv', 'process_priv',
            'reload_priv', 'repl_client_priv', 'repl_slave_priv', 'create_routine_priv',
            'alter_routine_priv', 'create_tablespace_priv', 'show_db_priv',
            'shutdown_priv', 'super_priv', 'proc_priv', 'table_priv', 'column_priv',
        ]
        for priv in cols:
            if priv in curp.keys():
                continue
            curp_val = curp.get(priv)
            try:
                u_val = getattr(u, priv)
            except AttributeError:
                u_val = None
                
            if priv == 'proc_priv' and u.proc_perm:
                curp_val = set(map(lambda x: (x.replace(' ', '_') + '_priv').lower(), curp.get('proc_priv').split(',')))
                u_val = u.perms_set
            if priv == 'table_priv' and u.table_perm:
                curp_val = set(map(lambda x: (x.replace(' ', '_') + '_priv').lower(), curp.get('table_priv').split(',')))
                u_val = u.perms_set
            if priv == 'column_priv' and u.column_perm:
                curp_val = set(map(lambda x: (x.replace(' ', '_') + '_priv').lower(), curp.get('column_priv').split(',')))
                u_val = u.perms_set
            if u_val != curp_val:
                changed = True
                break
        # User changed
        if changed:
            curp.update({
                'permtype': u.permtype,
                'server': rd.host,
                'created_at': u.created_at,
                'updated_at': rd.run_time,
                'run_time': rd.run_time,
            })
            hs = curp.copy()
            if 'timestamp' in hs.keys():
                hs['updated_at'] = hs.get('timestamp')
                hs.pop('timestamp')
            if u.table_perm:
                hs.pop('table_priv')
                hs.pop('column_priv')
            elif u.column_perm:
                hs.pop('column_priv')
            elif u.proc_perm:
                hs.pop('proc_priv')
            
            newu = rd.stat(**hs)
            if u.table_perm:
                newu.perms_fromsetstr(curp.get('table_priv'))
            elif u.column_perm:
                newu.perms_fromsetstr(curp.get('column_priv'))
            elif u.proc_perm:
                newu.perms_fromsetstr(curp.get('proc_priv'))
            newu.save()
            rd.stat_updated(newu.id, u.id)

Collector(TableUser, "user privilige tracking", action)

def for_action(stream, data, options):
    col_width = options.get('display_width', 80)
    server = str(data.server) if data.server is not None else ''
    if not options.get('header', False):
        stream.write('{1:15} {2:{0}}\n'.format(col_width-15, server, data))
    else:
        stream.write('{1:15} {2:{0}}\n'.format(col_width-15, 'host', 'grant'))

Formatter.proc_for('user', 'text', for_action)
