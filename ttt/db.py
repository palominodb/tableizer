import warnings

from django.core.management import call_command

import MySQLdb

class Db:
    app_config = None
    
    @classmethod
    def open(cls, opts):
        cls.app_config = opts
        
    @classmethod
    def open_schema(cls, host, schema):
        dsn = cls.app_config.get('dsn_connection')
        dsn.update({
            'host': host,
            'db': schema,
            'cursorclass': MySQLdb.cursors.DictCursor,
        })
        connection = MySQLdb.connect(**dsn)
        return connection
        
    @classmethod
    def migrate(cls):
        config = cls.app_config
        if config.get('ttt_connection', {}).get('adapter') == 'mysql':
            if config.get('ttt_connection', {}).get('host') is None or \
                    config.get('ttt_connection', {}).get('username') is None or \
                    config.get('ttt_connection', {}).get('password') is None:
                raise Exception, 'ttt_connection host, username and password are required.'
            db = MySQLdb.connect(
                host=config.get('ttt_connection').get('host'),
                user=config.get('ttt_connection').get('username'),
                passwd=config.get('ttt_connection').get('password')
            )
            
            c = db.cursor()
            warnings.filterwarnings('ignore')   # turn warnings off for MySQLdb
            c.execute(
                '''
                    CREATE DATABASE IF NOT EXISTS ttt;
                '''
            )
            db.close()
        
        call_command('syncdb', verbosity=1, noinput=False, migrate=True)
