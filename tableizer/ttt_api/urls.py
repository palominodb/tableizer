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

from django.conf.urls import patterns, include, url

from ttt_api import views

urlpatterns = patterns('',
        url(r'^$', views.api_root, name='api_root'),

        url(r'^servers/$', views.ServerListAPIView.as_view(), name='api_server_list'),
        url(r'^servers/(?P<id>\d+)/$', views.ServerDetailAPIView.as_view(), name='api_server_detail'),
        
        url(r'^databases/$', views.DatabaseListAPIView.as_view(), name='api_database_list'),
        url(r'^databases/top/$', views.TopDatabasesAPIView.as_view(), name='api_top_databases'),
        url(r'^databases/(?P<id>\d+)/$', views.DatabaseDetailAPIView.as_view(), name='api_database_detail'),
        
        url(r'^tables/$', views.DatabaseTableListAPIView.as_view(), name='api_table_list'),
        url(r'^tables/top/$', views.TopTablesAPIView.as_view(), name='api_top_tables'),
        url(r'^tables/(?P<id>\d+)/$', views.DatabaseTableDetailAPIView.as_view(), name='api_table_detail'),
        
        url(r'^history/$', views.HistoryAPIView.as_view(), name='api_history'),
)
