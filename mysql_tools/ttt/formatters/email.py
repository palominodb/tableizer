from django.conf import settings

from ttt.formatter import Formatter

class EmailFormatter(Formatter):
    
    def format_defn(self, stream, rows, *args):
        import time
        from django.core.urlresolvers import reverse
        from django.db.models import get_model
        DatabaseTable = get_model('ttt', 'DatabaseTable')
        link_url = ''
        # If include_links is set, then we'll need the gui_url.
        include_links = self.want_option('include_links', False)
        if include_links:
            link_url = self.need_option('gui_url')
            if link_url.endswith('/'):
                link_url = link_url[:-1]
        last_run = None
        for r in rows:
            tbl = DatabaseTable.objects.get(name=r.table_name, schema__name=r.database_name, schema__server__name=r.server)
            relative_url = reverse('table_detail', kwargs={'id':tbl.id})
            if last_run != r.run_time:
                stream.write('--- %s\n' % (str(r.run_time)))
                last_run = r.run_time
            if include_links:
                stream.write('{0}\t{1}.{2}.{3}\t({4}{5}?show_diff=true&at={6})\n'.format(
                    r.status,
                    r.server,
                    r.database_name,
                    r.table_name,
                    link_url,
                    relative_url,
                    int(time.mktime(r.run_time.timetuple())),
                ))
            else:
                stream.write('{0}\t{1}.{2}.{3}\n'.format(r.status, r.server, r.database_name, r.table_name))
    
    def format_user(self, stream, rows, *args):
        last_run = None
        for r in rows:
            if last_run != r.run_time:
                stream.write('--- %s\n' % (str(r.run_time)))
                stream.write('{0:15}         {1:15}\n'.format('host', 'grant'))
                last_run = r.run_time
            stream.write('{0:15}         {1:15}\n'.format(r.server, r))
            
    def format_volume(self, stream, rows, *args):
        last_run = None
        for r in rows:
            if last_run != r.run_time:
                stream.write('--- %s\n' % (str(r.run_time)))
                last_run = r.run_time
            stream.write('{0}\t{1}.{2}.{3}\t{4}mb\n'.format(r.status, str(r.server), str(r.database_name), str(r.table_name), 
                            (r.data_length + r.index_length)/1024/1024 if r.data_length is not None and r.index_length is not None else ''))
    
    def format(self, rows, *args):
        import StringIO
        from django.core import mail
        from django.db.models import get_model
        TableDefinition = get_model('ttt', 'TableDefinition')
        TableView = get_model('ttt', 'TableView')
        TableUser = get_model('ttt', 'TableUser')
        TableVolume = get_model('ttt', 'TableVolume')
        formatter_options = settings.FORMATTER_OPTIONS
        stream = self.stream
        args = list(args)
        options = self.__extract_options__(args)
        if 'email' not in formatter_options.keys():
            stream.write('[error]: Need email formatter options set to send email!\n')
            return False
            
        changes=0
        for row in rows:
            if row.__class__.objects.tchanged(row):
                changes += 1
                
        if 'send_empty' in formatter_options.get('email', {}).keys():
            if not formatter_options.get('email', {}).get('send_empty', False) and changes == 0:
                return True
                
        tstream = StringIO.StringIO()
        if rows[0].__class__ in [TableDefinition, TableView]:
            self.format_defn(tstream, rows, args)
        elif rows[0].__class__ == TableUser:
            self.format_user(tstream, rows, args)
        elif rows[0].__class__ == TableVolume:
            self.format_volume(tstream, rows, args)
        else:
            raise Exception, 'Unable to handle this record type: %s' % (rows[0].__class__)
            
        subj_prefix = '[MySQL Tools]'
        if 'subjectprefix' in formatter_options.get('email', {}).keys():
            subj_prefix = formatter_options.get('email', {}).get('subjectprefix')
        
        if 'emailto' not in formatter_options.get('email', {}).keys():
            tstream.write('[error]: Need \'formatter_options.email.emailto\' to send mail!\n')
            return False
            
        delivery_method = formatter_options.get('email', {}).get('delivery_method', 'sendmail')
        if delivery_method == 'sendmail':
            location = formatter_options.get('email', {}).get('sendmail_settings', {}).get('location', '/usr/sbin/sendmail')
            connection = mail.get_connection('ttt_email.backends.sendmail.EmailBackend')
            connection.location = location
        elif delivery_method == 'smtp':
            smtp_settings = formatter_options.get('email', {}).get('smtp_settings', {})
            host = smtp_settings.get('host', '')
            port = smtp_settings.get('port', '')
            username = smtp_settings.get('user', '')
            password = smtp_settings.get('password', '')
            use_tls = smtp_settings.get('use_tls', False)
            connection = mail.get_connection('django.core.mail.backends.smtp.EmailBackend')
            connection.host = host
            connection.port = port
            connection.username = username
            connection.password = password
            connection.use_tls = use_tls
        else:
            return False
        
        connection.open()
        to_email = formatter_options.get('email', {}).get('emailto', '')
        tstream_val = tstream.getvalue()
        body = '%s changes:\n%s' % (rows[0].__class__.collector, tstream_val)
        email = mail.EmailMessage(subj_prefix, body, 'ttt@localhost',
                                    [to_email], connection=connection)
        email.send()
        
        connection.close()
        
        return True
    
EmailFormatter.runner_for('email')
