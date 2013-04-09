import MySQLdb

from tableizer import settings
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
