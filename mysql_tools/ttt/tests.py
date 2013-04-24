import sys

from django.test import TestCase

from .models import TableDefinition, TableView, TableVolume, TableUser
from .formatter import Formatter
from utilities.utils import flatten, humanize, titleize, get_db_key

class UtilitiesTestCase(TestCase):

    def test_flatten(self):
        sample_list = [[1,[2],[3, [4, [5]]]]]
        flat_list = [1,2,3,4,5]
        self.assertEqual(flat_list, list(flatten(sample_list)))
        
    def test_humanize(self):
        string = 'hello_world'
        self.assertEqual('Hello World', humanize(string))
        
    def test_humanize2(self):
        string = 'hello_world'
        self.assertEqual('Hello world', humanize(string, uppercase='first'))
        
    def test_titleize(self):
        string = 'HelloWorld'
        self.assertEqual('Hello World', titleize(string))
        
    def test_humanize2(self):
        string = 'hello_world'
        self.assertEqual('Hello world', titleize(string, uppercase='first'))
        
    def test_get_db_key(self):
        sample_dict = {
            'localhost_information_schema': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'information_schema',
                'USER': 'user',
                'PASSWORD': 'password',
                'HOST': 'localhost',
                'PORT': '',
            },
        }
        with self.settings(TABLEIZER_DBS=sample_dict):
            self.assertEqual('localhost_information_schema', get_db_key('localhost'))
            
class FormattersTestCase(TestCase):
    
    def setUp(self):
        self.sample_dict = {
            'global': (
                'localhost\.mysql\..*',
            ),
            'definition': (
                '.*\.definition\..*',
            ),
            'view': (
                '.*\.view\..*',
            ),
            'volume': (
                '.*\.volume\..*',
            ),
            'user': (
                '.*\.user\..*',
            ),
        }
        self.definition_list = [
            TableDefinition(server='localhost', database_name='db1', table_name='table1'),
            TableDefinition(server='localhost', database_name='mysql', table_name='table1'),
            TableDefinition(server='localhost', database_name='definition', table_name='table1'),
            TableDefinition(server='localhost', database_name='db2', table_name='table1'),
            TableDefinition(server='localhost', database_name='definition', table_name='table2'),
        ]
        self.volume_list = [
            TableVolume(server='localhost', database_name='db1', table_name='table1'),
            TableVolume(server='localhost', database_name='mysql', table_name='table1'),
            TableVolume(server='localhost', database_name='volume', table_name='table1'),
            TableVolume(server='localhost', database_name='db2', table_name='table1'),
            TableVolume(server='localhost', database_name='volume', table_name='table2'),
        ]
        self.view_list = [
            TableView(server='localhost', database_name='db1', table_name='table1'),
            TableView(server='localhost', database_name='mysql', table_name='table1'),
            TableView(server='localhost', database_name='view', table_name='table1'),
            TableView(server='localhost', database_name='db2', table_name='table1'),
            TableView(server='localhost', database_name='view', table_name='table2'),
        ]
        self.user_list = [
            TableUser(server='localhost', db='db1', table_name='table1'),
            TableUser(server='localhost', db='mysql', table_name='table1'),
            TableUser(server='localhost', db='user', table_name='table1'),
            TableUser(server='localhost', db='db2', table_name='table1'),
            TableUser(server='localhost', db='user', table_name='table2'),
        ]

    def test_reject_ignores_definition(self):
        with self.settings(REPORT_IGNORE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.reject_ignores(self.definition_list)
            expected_output = [
                TableDefinition(server='localhost', database_name='db1', table_name='table1'),
                TableDefinition(server='localhost', database_name='db2', table_name='table1'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_reject_ignores_view(self):
        with self.settings(REPORT_IGNORE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.reject_ignores(self.view_list)
            expected_output = [
                TableView(server='localhost', database_name='db1', table_name='table1'),
                TableView(server='localhost', database_name='db2', table_name='table1'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_reject_ignores_volume(self):
        with self.settings(REPORT_IGNORE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.reject_ignores(self.volume_list)
            expected_output = [
                TableVolume(server='localhost', database_name='db1', table_name='table1'),
                TableVolume(server='localhost', database_name='db2', table_name='table1'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_reject_ignores_user(self):
        with self.settings(REPORT_IGNORE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.reject_ignores(self.user_list)
            expected_output = [
                TableUser(server='localhost', db='db1', table_name='table1'),
                TableUser(server='localhost', db='db2', table_name='table1'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_report_include_definition(self):
        with self.settings(REPORT_INCLUDE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.report_include(self.definition_list)
            expected_output = [
                TableDefinition(server='localhost', database_name='mysql', table_name='table1'),
                TableDefinition(server='localhost', database_name='definition', table_name='table1'),
                TableDefinition(server='localhost', database_name='definition', table_name='table2'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_report_include_view(self):
        with self.settings(REPORT_INCLUDE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.report_include(self.view_list)
            expected_output = [
                TableView(server='localhost', database_name='mysql', table_name='table1'),
                TableView(server='localhost', database_name='view', table_name='table1'),
                TableView(server='localhost', database_name='view', table_name='table2'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_report_include_volume(self):
        with self.settings(REPORT_INCLUDE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.report_include(self.volume_list)
            expected_output = [
                TableVolume(server='localhost', database_name='mysql', table_name='table1'),
                TableVolume(server='localhost', database_name='volume', table_name='table1'),
                TableVolume(server='localhost', database_name='volume', table_name='table2'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_report_include_user(self):
        with self.settings(REPORT_INCLUDE=self.sample_dict):
            formatter = Formatter(sys.stdout)
            output = formatter.report_include(self.user_list)
            expected_output = [
                TableUser(server='localhost', db='mysql', table_name='table1'),
                TableUser(server='localhost', db='user', table_name='table1'),
                TableUser(server='localhost', db='user', table_name='table2'),
            ]
            self.assertEqual(output, expected_output)
            
    def test_need_option(self):
        with self.settings(FORMATTER_OPTIONS={}):
            formatter = Formatter(sys.stdout)
            formatter.media = 'rrd'
            with self.assertRaises(NameError):
                formatter.need_option('interval')
                
    def test_need_option2(self):
        with self.settings(FORMATTER_OPTIONS={'rrd':{'interval':'2m'}}):
            formatter = Formatter(sys.stdout)
            formatter.media = 'rrd'
            output = formatter.need_option('interval')
            expected_output = '2m'
            self.assertEqual(output, expected_output)
            
    def test_want_option(self):
        with self.settings(FORMATTER_OPTIONS={}):
            formatter = Formatter(sys.stdout)
            formatter.media = 'rrd'
            output = formatter.want_option('interval', '2m')
            expected_output = '2m'
            self.assertEqual(output, expected_output)
            
    def test_want_option2(self):
        with self.settings(FORMATTER_OPTIONS={'rrd':{'interval':'2m'}}):
            formatter = Formatter(sys.stdout)
            formatter.media = 'rrd'
            output = formatter.want_option('interval')
            expected_output = '2m'
            self.assertEqual(output, expected_output)
