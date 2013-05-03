# diff_tags.py
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
