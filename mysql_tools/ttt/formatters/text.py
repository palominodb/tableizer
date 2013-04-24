# text.py
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
from ttt.formatter import Formatter

class TextFormatter(Formatter):

    def format(self, rows, *args):
        args = list(args)
        options = self.__extract_options__(args)
        stream = self.stream
        run_time = None
        options['display_width'] = 80 if options.get('display_width') is None else options.get('display_width')
            
        for row in rows:
            if row.run_time != run_time:
                if run_time is not None:
                    stream.write('')
                stream.write('-- {0} '.format(row.run_time) + '-'*(120 if options.get('display_width', 80)-26 > 120 else options.get('display_width', 80)-26) + '\n')
                run_time = row.run_time
                formatter = self.get_formatter_for(row.collector)
                if formatter is not None:
                    options_clone = options.copy()
                    options_clone.update({'header': True})
                    formatter(stream, row, options_clone)
            formatter = self.get_formatter_for(row.collector)
            if formatter is not None:
                formatter(stream, row, options)
        return 0

TextFormatter.runner_for('text')
