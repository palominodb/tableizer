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
