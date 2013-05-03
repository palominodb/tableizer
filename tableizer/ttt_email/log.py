# log.py
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
import logging

from django.conf import settings
from django.core import mail


class CrashHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        if not settings.PDB_ADMINS:
            return
        
        formatter_options = settings.FORMATTER_OPTIONS
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
        subj_prefix = 'Tableizer Crashed'    
        body = 'Attached is a backtrace of the exception.'
        email = mail.EmailMessage(subj_prefix, body, settings.SERVER_EMAIL,
                                    [a[1] for a in settings.PDB_ADMINS], connection=connection)
        email.attach('%s_traceback.txt' % (settings.SERVER_EMAIL), record.getMessage())
        email.send()
        connection.close()
        return True
