# db.py
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
from django.conf import settings

import MySQLdb

from utilities.utils import get_db_key

class Db(object):
    
    @classmethod
    def open_schema(cls, host, schema):
        k = get_db_key(host)
        db = settings.TABLEIZER_DBS.get(k)
        conn_dict = {
            'host': host,
            'db': schema,
            'cursorclass': MySQLdb.cursors.DictCursor,
            'user': db.get('USER', ''),
            'passwd': db.get('PASSWORD', ''),
        }
        port = db.get('PORT', '')
        if port != '':
            conn_dict.update({
                'port': int(port)
            })
        connection = MySQLdb.connect(**conn_dict)
        return connection
