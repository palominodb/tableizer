# serializers.py
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

from rest_framework import serializers
from rest_framework.reverse import reverse

from ttt.models import Server, ServerSchema, DatabaseTable, TableDefinition, \
                        TableView, TableVolume, TableUser

class DatabaseTableListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_table_detail_url')
    server = serializers.SerializerMethodField('get_server_id')
    
    class Meta:
        model = DatabaseTable
        
    def get_table_detail_url(self, obj):
        return reverse('api_table_detail', kwargs={'id':obj.id}, request=self.context.get('request'))
        
    def get_server_id(self, obj):
        return obj.schema.server.id
        
class DatabaseTableDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseTable

class DatabaseListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_database_detail_url')
    tables = serializers.PrimaryKeyRelatedField(source='databasetable_set', many=True)
    
    class Meta:
        model = ServerSchema
        
    def get_database_detail_url(self, obj):
        return reverse('api_database_detail', kwargs={'id':obj.id}, request=self.context.get('request'))
        
class DatabaseDetailSerializer(serializers.ModelSerializer):
    tables = DatabaseTableListSerializer(source='databasetable_set', many=True)
    
    class Meta:
        model = ServerSchema

class ServerListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_server_detail_url')
    databases = serializers.PrimaryKeyRelatedField(source='serverschema_set', many=True)

    class Meta:
        model = Server
        
    def get_server_detail_url(self, obj):
        return reverse('api_server_detail', kwargs={'id':obj.id}, request=self.context.get('request'))
        
class ServerDetailSerializer(serializers.ModelSerializer):
    databases = DatabaseListSerializer(source='serverschema_set', many=True)
    
    class Meta:
        model = Server
        
class TableDefinitionSerializer(serializers.ModelSerializer):
    diff = serializers.SerializerMethodField('get_diff')
    status = serializers.SerializerMethodField('get_status')
    
    class Meta:
        model = TableDefinition
        
    def get_diff(self, obj):
        try:
            prev_version = obj.previous_version
            if prev_version is None:
                prev_create_syntax = []
            else:
                prev_create_syntax = prev_version.create_syntax.split('\n')
            diff = difflib.unified_diff(prev_create_syntax, obj.create_syntax.split('\n'))
            result = list(diff)
            result.pop(0)
            result.pop(1)
            result.insert(0, '--- %s\t%s' % (str(obj.table_name), str(obj.prev_stat_created_at)))
            result.insert(1, '+++ %s\t%s' % (str(obj.table_name), str(obj.stat_created_at)))
            return '\n'.join(d.strip() for d in result)
        except Exception, e:
            return ''
            
    def get_status(self, obj):
        return obj.status
        
class TableViewSerializer(serializers.ModelSerializer):
    diff = serializers.SerializerMethodField('get_diff')
    status = serializers.SerializerMethodField('get_status')
    
    class Meta:
        model = TableView
        
    def get_diff(self, obj):
        try:
            prev_version = obj.previous_version
            if prev_version is None:
                prev_create_syntax = []
            else:
                prev_create_syntax = prev_version.create_syntax.split('\n')
            diff = difflib.unified_diff(prev_create_syntax, obj.create_syntax.split('\n'))
            result = list(diff)
            result.pop(0)
            result.pop(1)
            result.insert(0, '--- %s\t%s' % (str(obj.table_name), str(obj.prev_stat_created_at)))
            result.insert(1, '+++ %s\t%s' % (str(obj.table_name), str(obj.stat_created_at)))
            return '\n'.join(d.strip() for d in result)
        except Exception, e:
            print e
            return ''
        
    def get_status(self, obj):
        return obj.status
        
class TableVolumeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    
    class Meta:
        model = TableVolume
        
    def get_status(self, obj):
        return obj.status
        
class TableUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_string')
    status = serializers.SerializerMethodField('get_status')
    
    class Meta:
        model = TableUser
        fields = ('server', 'status', 'user')
    
    def get_user_string(self, obj):
        return str(obj)
            
    def get_status(self, obj):
        return obj.status
