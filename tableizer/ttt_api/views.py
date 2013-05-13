# views.py
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
import itertools
import math
from datetime import datetime, timedelta

from django.db.models import Max, Min

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from ttt_api import serializers
from ttt.models import Server, ServerSchema, DatabaseTable, TableDefinition, \
                        TableView, TableVolume, TableUser
from utilities.utils import str_to_datetime

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'servers': reverse('api_server_list', request=request),
        'databases': reverse('api_database_list', request=request),
        'tables': reverse('api_table_list', request=request),
        'history': reverse('api_history', request=request),
        'top_databases': reverse('api_top_databases', request=request),
        'top_tables': reverse('api_top_tables', request=request),
    })

class ServerListAPIView(generics.ListAPIView):
    '''
        API for fetching all Servers.
    '''
    model = Server
    serializer_class = serializers.ServerListSerializer
    
class ServerDetailAPIView(generics.RetrieveAPIView):
    '''
        API for fetching server data.
    '''
    model = Server
    serializer_class = serializers.ServerDetailSerializer
    pk_url_kwarg = 'id'
    
class DatabaseListAPIView(generics.ListAPIView):
    '''
        API for fetching all Databases.
    '''
    model = ServerSchema
    serializer_class = serializers.DatabaseListSerializer
    
class DatabaseDetailAPIView(generics.RetrieveAPIView):
    '''
        API for fetching database data.
    '''
    model = ServerSchema
    serializer_class = serializers.DatabaseDetailSerializer
    pk_url_kwarg = 'id'
    
class DatabaseTableListAPIView(generics.ListAPIView):
    '''
        API for fetching all Tables.
    '''
    model = DatabaseTable
    serializer_class = serializers.DatabaseTableListSerializer
    
class DatabaseTableDetailAPIView(generics.RetrieveAPIView):
    '''
        API for fetching table data.
    '''
    model = DatabaseTable
    serializer_class = serializers.DatabaseTableDetailSerializer
    pk_url_kwarg = 'id'
    
class HistoryAPIView(generics.GenericAPIView):
    '''
        API for tracking tableizer history. This is similar to the tableizer-query management command.
        Accepts parameters 'since' and 'stat' and uses it the same way as the tableizer-query command.
    '''
    
    def get(self, request, *args, **kwargs):
        since_string = self.request.QUERY_PARAMS.get('since', '72h')
        stat = self.request.QUERY_PARAMS.get('stat')
        return_dict = {}        
        if not stat:
            stat = 'definition'
        since = str_to_datetime(since_string)
        if stat == 'definition':
            definitions = self.get_definitions(since)
            return_dict.update({'definitions': definitions})
        elif stat == 'view':
            views = self.get_views(since)
            return_dict.update({'views': views})
        elif stat == 'volume':
            volumes = self.get_volumes(since)
            return_dict.update({'volumes': volumes})
        elif stat == 'user':
            users = self.get_users(since)
            return_dict.update({'users': users})
        elif stat == 'all':
            definitions = self.get_definitions(since)
            views = self.get_views(since)
            volumes = self.get_volumes(since)
            users = self.get_users(since)
            return_dict.update({
                'definitions': definitions,
                'views': views,
                'volumes': volumes,
                'users': users,
            })
        return Response(return_dict)
        
    def get_definitions(self, since):
        tables = TableDefinition.objects.filter(run_time__gt=since).order_by('-run_time')
        grouped_tables = itertools.groupby(tables, key=lambda x: x.run_time)
        definitions = {}
        for key,group in grouped_tables:
            defns = serializers.TableDefinitionSerializer(list(group), many=True)
            definitions.update({str(key): defns.data})
        return definitions
        
    def get_views(self, since):
        views = TableView.objects.filter(run_time__gt=since).order_by('-run_time')
        grouped_views = itertools.groupby(views, key=lambda x: x.run_time)
        views = {}
        for key,group in grouped_views:
            defns = serializers.TableViewSerializer(list(group), many=True)
            views.update({str(key): defns.data})
        return views
        
    def get_volumes(self, since):
        volumes = TableVolume.objects.filter(run_time__gt=since).order_by('-run_time')
        grouped_volumes = itertools.groupby(volumes, key=lambda x: x.run_time)
        volumes = {}
        for key,group in grouped_volumes:
            defns = serializers.TableVolumeSerializer(list(group), many=True)
            volumes.update({str(key): defns.data})
        return volumes
        
    def get_users(self, since):
        users = TableUser.objects.filter(run_time__gt=since).order_by('-run_time')
        grouped_users = itertools.groupby(users, key=lambda x: x.run_time)
        users = {}
        for key,group in grouped_users:
            defns = serializers.TableUserSerializer(list(group), many=True)
            users.update({str(key): defns.data})
        return users
        
class TopDatabasesAPIView(generics.GenericAPIView):
    '''
        API for fetching top databases. This accepts 'percent', 'gbytes', 'lim' and 'days' as parameters.
    '''
    
    def get(self, request, *args, **kwargs):
        return_dict = {}
        percent = request.QUERY_PARAMS.get('percent')
        gbytes = request.QUERY_PARAMS.get('gbytes')
        days = request.QUERY_PARAMS.get('days')
        lim = request.QUERY_PARAMS.get('lim')
        raw_tables = {}
        
        if percent is None:
            percent = float('nan')
        else:
            percent = float(percent)
        
        if gbytes is None:
            gbytes = float('nan')
        else:
            gbytes = float(gbytes)
        
        if days is None:
            dt = datetime.min
        else:
            days = int(days)
            dt = datetime.now() - timedelta(days=days)
            
        if lim is not None:
            lim = int(lim)
        
        if not math.isnan(percent):
            min_maxes = TableVolume.objects.exclude(database_name=None, 
                table_name=None).filter(run_time__gt=dt).values('server',
                'database_name', 'table_name').annotate(min_id=Min('id'), max_id=Max('id'))
            
            for t in min_maxes:
                min_tbl = TableVolume.objects.get_or_none(id=t.get('min_id'))
                max_tbl = TableVolume.objects.get_or_none(id=t.get('max_id'))
                
                if min_tbl is None or max_tbl is None or min_tbl.deleted or max_tbl.deleted:
                    continue
                if [min_tbl.server, min_tbl.database_name] not in raw_tables.keys():
                    raw_tables[(min_tbl.server, min_tbl.database_name)] = 0.0
                if min_tbl.size != 0:
                    raw_tables[(min_tbl.server, min_tbl.database_name)] += (max_tbl.size+0.0-min_tbl.size+0.0)/min_tbl.size+0.0
                
            raw_array = [[k, v] for k,v in raw_tables.items()]
            raw_array = filter(lambda x: x[1] > percent, raw_array)
            raw_array.sort(key=lambda x: -x[1])
            
            if lim is not None:
                raw_array = raw_array[:lim]
            
            return_dict.update({'type': 'top_Pct'})
            dict_array = []
            
            for element in raw_array:
                dict_array.append({
                    'server': element[0][0],
                    'database': element[0][1],
                    'percent_growth': element[1],
                })
            return_dict.update({'databases': dict_array})
        elif not math.isnan(gbytes):
            min_maxes = TableVolume.objects.exclude(database_name=None, 
                table_name=None).filter(run_time__gt=dt).values('server',
                'database_name', 'table_name').annotate(min_id=Min('id'), max_id=Max('id'))
            
            for t in min_maxes:
                min_tbl = TableVolume.objects.get_or_none(id=t.get('min_id'))
                max_tbl = TableVolume.objects.get_or_none(id=t.get('max_id'))
                
                if min_tbl is None or max_tbl is None or min_tbl.deleted or max_tbl.deleted:
                    continue
                if [min_tbl.server, min_tbl.database_name] not in raw_tables.keys():
                    raw_tables[(min_tbl.server, min_tbl.database_name)] = 0.0
                
            raw_tables[(min_tbl.server, min_tbl.database_name)] += (max_tbl.size+0.0-min_tbl.size+0.0)
            raw_array = [[k, v] for k,v in raw_tables.items()]
            raw_array = filter(lambda x: x[1] > gbytes*(1024**3), raw_array)
            raw_array.sort(key=lambda x: -x[1])
            
            if lim is not None:
                raw_array = raw_array[:lim]
            
            return_dict.update({'type': 'top_GB'})
            dict_array = []
            
            for element in raw_array:
                dict_array.append({
                    'server': element[0][0],
                    'database': element[0][1],
                    'gb_growth': element[1],
                })
            return_dict.update({'databases': dict_array})
        else:
            return_dict.update({
                'error': '\'percent\' or \'gbytes\' parameter is required'
            })
        return Response(return_dict)
        
class TopTablesAPIView(generics.GenericAPIView):
    '''
        API for fetching top tables. This accepts 'server', 'db', 'percent', 'lim' and 'days' as parameters.
    '''
    def get(self, request, *args, **kwargs):
        return_dict = {}
        s_id = request.QUERY_PARAMS.get('server')
        d_id = request.QUERY_PARAMS.get('db')
        percent = request.QUERY_PARAMS.get('percent')
        days = request.QUERY_PARAMS.get('days')
        lim = request.QUERY_PARAMS.get('lim')
        srv = Server.objects.get_or_none(id=s_id)
        db = ServerSchema.objects.get_or_none(id=d_id)
        
        if percent is None:
            percent = float('nan')
        else:
            percent = float(percent)
        
        if days is None:
            dt = datetime.min
        else:
            days = int(days)
            dt = datetime.now() - timedelta(days=days)
        
        if lim is not None:
            lim = int(lim)
        
        if days != 0 and not math.isnan(percent):
            raw_tables = {}
            min_maxes = TableVolume.objects.exclude(database_name=None,
                table_name=None).filter(run_time__gt=dt)
            
            if srv is not None:
                min_maxes = min_maxes.filter(server=srv.name)
            min_maxes = min_maxes.values('server', 'database_name', 'table_name').annotate(min_id=Min('id'), max_id=Max('id'))
            
            for t in min_maxes:
                min_tbl = TableVolume.objects.get_or_none(id=t.get('min_id'))
                max_tbl = TableVolume.objects.get_or_none(id=t.get('max_id'))
                if min_tbl is None or max_tbl is None or min_tbl.deleted or max_tbl.deleted:
                    continue
                if min_tbl.size != 0:
                    raw_tables[(min_tbl.server, min_tbl.database_name, min_tbl.table_name)] = (max_tbl.size+0.0-min_tbl.size+0.0)/min_tbl.size+0.0
            
            raw_array = [[k, v] for k,v in raw_tables.items()]
            raw_array = filter(lambda x: x[1] > percent, raw_array)
            raw_array.sort(key=lambda x: -x[1])
            
            if lim is not None:
                raw_array = raw_array[:lim]
            return_dict.update({'type': 'top_Pct'})
            dict_array = []
            
            for element in raw_array:
                dict_array.append({
                    'server': element[0][0],
                    'database': element[0][1],
                    'table': element[0][2],
                    'percent_growth': element[1],
                })
            return_dict.update({'databases': dict_array})    
        else:
            if s_id is None:
                tables = DatabaseTable.objects.all().order_by('-cached_size')
            else:
                if d_id is None:
                    tables = DatabaseTable.objects.filter(schema__server__id=s_id).order_by('-cached_size')
                else:
                    tables = DatabaseTable.objects.filter(schema__id=d_id, schema__server__id=s_id).order_by('-cached_size')
            
            if lim is not None and lim != 0:
                tables = tables[:lim]
            
            return_dict.update({'type': 'top_N'})
            dict_array = []
            
            for element in tables:
                dict_array.append({
                    'server': element.schema.server.name,
                    'database': element.schema.name,
                    'table': element.name,
                    'cached_size': element.cached_size,
                })
            return_dict.update({'databases': dict_array})
        return Response(return_dict)
