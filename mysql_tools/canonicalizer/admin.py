# admin.py
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

from django.contrib import admin

import canonicalizer.models as app_models


class StatementDataAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'dt', 'statement', 'hostname', 'server_id',
        'canonicalized_statement', 'canonicalized_statement_hash_hex_str',
        'canonicalized_statement_hostname_hash_hex_str',
        'query_time', 'lock_time', 'rows_sent', 'rows_examined',
        'rows_affected', 'rows_read', 'bytes_sent',
        'tmp_tables', 'tmp_disk_tables', 'tmp_table_sizes', 'schema',
        'sequence_id',
        'created_at', 'updated_at')


class ExplainResultInline(admin.TabularInline):
    model = app_models.ExplainResult


class ExplainedStatementAdmin(admin.ModelAdmin):
    inlines = [ExplainResultInline,]
    list_display = (
        'id', 'dt', 'statement', 'server_id', 'canonicalized_statement',
        'canonicalized_statement_hash_hex_str',
        'canonicalized_statement_hostname_hash_hex_str',
        'db',
        'created_at', 'updated_at')


admin.site.register(app_models.StatementData, StatementDataAdmin)
admin.site.register(app_models.ExplainedStatement, ExplainedStatementAdmin)
