import glob
import os
import re

from django.conf import settings

from ttt.collector import CollectorRegistry

class Formatter:
    loaded_formatters = False
    formatters = {}
    runners = {}
    
    def __init__(self, stream):
        self.stream = stream
        
    def __extract_options__(self, param):
        if len(param) > 0:
            if isinstance(param[-1], dict):
                val = param.pop(-1)
                return val
        return {}
        
    def format(self, rows, *args):
        raise Exception, "Use a real formatter."
    
    def reject_ignores(self, rows):
        try:
            report_ignore = settings.REPORT_IGNORE
        except Exception, e:
            return rows
        return_rows = []
        for r in rows:
            server_schema_table = '.'.join([r.server if r.server is not None else '', r.database_name if r.database_name is not None else '', 
                                            r.table_name if r.table_name is not None else ''])
            do_rej = False
            if report_ignore.get(r.collector) is not None:
                for reg in report_ignore.get(r.collector, []):
                    re_match = re.search(reg, server_schema_table)
                    if re_match is not None:
                        do_rej = True
                        break
            if not do_rej:
                if report_ignore.get('global') is not None:
                    for reg in report_ignore.get('global', []):
                        re_match = re.search(reg, server_schema_table)
                        if re_match is not None:
                            do_rej = True
                            break
            if not do_rej:
                return_rows.append(r)
        return return_rows
      
    def need_option(self, key):
        formatter_options = settings.FORMATTER_OPTIONS
        if str(self.media) not in formatter_options.keys() or key not in formatter_options.get(self.media, {}).keys():
            raise NameError, "Missing formatter_options.%s.%s in config." % (self.media, key)
        return formatter_options.get(str(self.media), {}).get(key)
    
    def want_option(self, key, value=None):
        formatter_options = settings.FORMATTER_OPTIONS
        if key in formatter_options.get(self.media, {}).keys():
            return formatter_options.get(self.media, {}).get(key)
        else:
            return value
    
    @classmethod
    def proc_for(cls, collector, output_media, action):
        if Formatter.formatters.get(collector) is None:
            Formatter.formatters[collector] = {}
        Formatter.formatters[collector][output_media] = action
    
    @classmethod
    def runner_for(cls, media):
        Formatter.runners[media] = cls
        cls.media = media
        return cls.media
        
    @staticmethod
    def get_runner_for(media):
        Formatter.load_all()
        return Formatter.runners[media]
        
    def get_formatter_for(self, collector, mtype=None):
        mtype = self.media
        CollectorRegistry.load()
        return Formatter.formatters.get(collector, {}).get(mtype)
        
    @staticmethod
    def load_all(from_path=os.path.join(os.path.dirname(__file__), 'formatters', '*')):
        if not Formatter.loaded_formatters:
            map(execfile, glob.glob(from_path+'.py'))
            Formatter.loaded_formatters = True
