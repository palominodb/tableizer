import difflib

from django import template

register = template.Library()

def gen_diff(value):
    try:
        prev_version = value.previous_version
        if prev_version is None:
            prev_create_syntax = []
        else:
            prev_create_syntax = prev_version.create_syntax.split('\n')
        diff = difflib.unified_diff(prev_create_syntax, value.create_syntax.split('\n'))
        result = list(diff)
        result.pop(0)
        result.pop(1)
        result.insert(0, '--- %s\t%s' % (str(value.table_name), str(value.prev_stat_created_at)))
        result.insert(1, '+++ %s\t%s' % (str(value.table_name), str(value.stat_created_at)))
        return '\n'.join(d.strip() for d in result)
    except Exception, e:
        return ''
        
register.filter('gen_diff', gen_diff)
