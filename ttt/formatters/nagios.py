import re

from ttt.formatter import Formatter

class NagiosFormatter(Formatter):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3    
    
    def format(self, rows, *args):
        import humanize
        cfg = self.cfg
        stream = self.stream
        args = list(args)
        options = self.__extract_options__(args)
        
        if 'formatter_options' not in cfg.keys() and 'nagios' not in cfg.get('formatter_options', {}).keys():
            stream.write('Must specify nagios formatter options in the config file.')
            return self.UNKNOWN
        
        do_alert = False
        alert_level = self.WARNING
        cfg_level = cfg.get('formatter_options', {}).get('nagios', {}).get('alert_level', '')
        if cfg_level == 'critical':
            alert_level = self.CRITICAL
        elif cfg_level == 'warning':
            alert_level = self.WARNING
        elif cfg_level == 'unknown':
            alert_level = self.UNKNOWN
        elif cfg_level == 'ok':
            alert_level = self.OK
        else:
            alert_level = self.WARNING
            
        tables = cfg.get('formatter_options', {}).get('nagios', {}).get('tables') if cfg.get('formatter_options', {}).get('nagios', {}).get('tables') else []
        real_rows = []
        output_str = ''
        
        if options.get('raw'):
            real_rows = rows
        else:
            real_rows = self.reject_ignores(rows)
            
        for row in real_rows:
            if row.__class__.objects.status(row) in ['changed', 'new', 'deleted', 'unreachable']:
                sst = '.'.join([row.server, row.database_name, row.table_name])
                row_alert = False
                for rex in tables:
                    if re.match(rex, sst) is not None:
                        do_alert = True
                        row_alert = True
                if row_alert:
                    output_str += '%s.%s(%s %s), ' % (row.database_name, row.table_name,
                                                            row.__class__.objects.status(row).upper(),
                                                            humanize.naturaltime(row.run_time))
        if output_str != '':
            print re.sub(', $', '', output_str)
            if do_alert:
                return alert_level
        else:
            print 'No changes.'
            return self.OK
            
NagiosFormatter.runner_for('nagios')
