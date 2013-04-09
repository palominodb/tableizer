import collections
import re
import time
from datetime import datetime, timedelta

from tableizer import settings

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def humanize(word, uppercase=''):
    if(uppercase == 'first'):
        return re.sub('_id$', '', word).replace('_', ' ').capitalize()
    else:
        return re.sub('_id$', '', word).replace('_', ' ').title()

def underscore(word):
    return re.sub('[^A-Z^a-z^0-9^\/]+', '_',
        re.sub('([a-z\d])([A-Z])', '\\1_\\2',
        re.sub('([A-Z]+)([A-Z][a-z])', '\\1_\\2', re.sub('::', '/', word)))).lower()
            
def titleize(word, uppercase=''):
    if(uppercase == 'first'):
        return humanize(underscore(word)).capitalize()
    else:
        return humanize(underscore(word)).title()
        
def str_to_datetime(string):
    regex = re.search('(\d+(?:\.?\d+)?)([hdwmHDWM])?', string)
    num, unit = regex.groups()
    unit = unit.lower()
    num = float(num)
    if unit == 'h':
        dtime = datetime.now() - timedelta(hours=num)
    elif unit == 'd':
        dtime = datetime.now() - timedelta(days=num)
    elif unit == 'w':
        dtime = datetime.now() - timedelta(weeks=num)
    elif unit == 'm':
        dtime = datetime.now() - timedelta(minutes=num)
    else:
        dtime = datetime.now() - timedelta(seconds=num)
    return dtime
    
def datetime_to_int(dtime):
    return int(time.mktime(dtime.timetuple()))
    
def get_db_key(host):
    dbs = settings.TABLEIZER_DBS
    for k,v in dbs.items():
        if host == v.get('HOST') or (host == 'localhost' and v.get('HOST') == ''):
            return k
