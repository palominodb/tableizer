# urls.py
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
from django.conf.urls import patterns, url

urlpatterns = patterns('canonicalizer.views',
        url(r'^$', 'home', name='canonicalizer_index'),

        url(r'^sparkline/(?P<data>.+)/$', 'sparkline', name='canonicalizer_sparkline'),
        
        url(r'^save-statement-data/', 'save_statement_data', name='save_statement_data'),
        url(r'^save-explained-statement/', 'save_explained_statement', name='save_explained_statement'),
        
        url(r'^last-statements/(?P<window_length>\d+)/', 'last_statements', name='last_statements'),
        url(r'^top-queries/(?P<n>\d+)/', 'top_queries', name='top_queries'),
        
        url(r'^explained-statements/', 'explained_statements', name='explained_statements'),
        url(r'^explain-results/(?P<id>\d+)/', 'explain_results', name='explain_results'),
)
