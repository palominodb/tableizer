import math
import re
from datetime import datetime, timedelta

from django.db.models import Max, Min
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .forms import TopDatabasesForm, TopTablesForm
from rrd import Rrdtool
from ttt.models import DatabaseTable, Server, ServerSchema, TableDefinition, TableView, \
                        TableVolume
from utilities.utils import str_to_datetime

class ServerListView(ListView):
    template_name = 'ttt_gui/servers/server_list.html'
    queryset = Server.objects.all()
    context_object_name = 'servers'
    
class ServerDetailView(DetailView):
    template_name = 'ttt_gui/servers/server_detail.html'
    context_object_name = 'server'
    
    def get_object(self, queryset=None):
        server = get_object_or_404(Server, id=self.kwargs.get('id'))
        since_string = self.request.session.get('since_string')
        r = Rrdtool()
        r.server_graph(server, since_string, 'full')
        return server
        
class DatabaseListView(ListView):
    template_name = 'ttt_gui/databases/database_list.html'
    queryset = ServerSchema.objects.all().order_by('-cached_size')
    context_object_name = 'databases'
    
class DatabaseDetailView(DetailView):
    template_name = 'ttt_gui/databases/database_detail.html'
    context_object_name = 'database'
    
    def get_object(self, queryset=None):
        db = get_object_or_404(ServerSchema, id=self.kwargs.get('id'))
        since_string = self.request.session.get('since_string')
        r = Rrdtool()
        r.database_graph(db, since_string, 'full')
        return db
        
class TableDetailView(DetailView):
    template_name = 'ttt_gui/tables/table_detail.html'
    context_object_name = 'table'
    
    def get_object(self, queryset=None):
        table = get_object_or_404(DatabaseTable, id=self.kwargs.get('id'))
        since_string = self.request.session.get('since_string')
        r = Rrdtool()
        r.table_graph(table, since_string , 'full')
        return table

    def get_context_data(self, **kwargs):
        context = super(TableDetailView, self).get_context_data(**kwargs)
        context['show_diff'] = self.request.GET.get('show_diff', False)
        return context
        
class HistoryIndexView(TemplateView):
    template_name = 'ttt_gui/history/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(HistoryIndexView, self).get_context_data(**kwargs)
        since_string = self.request.session.get('since_string')
        since = str_to_datetime(since_string)
        show_diff = self.request.GET.get('show_diff', 0)
        if show_diff == '1':
            context['show_diff'] = True
        else:
            context['show_diff'] = False
        context['tables'] = TableDefinition.objects.filter(run_time__gt=since).order_by('-run_time')
        context['views'] = TableView.objects.filter(run_time__gt=since).order_by('-run_time')
        return context
        
class ShowHistoryView(TemplateView):
    template_name = 'ttt_gui/history/show.html'
    
    def get_context_data(self, **kwargs):
        context = super(ShowHistoryView, self).get_context_data(**kwargs)
        table = get_object_or_404(DatabaseTable, id=self.kwargs.get('id'))
        show_diff = self.request.GET.get('show_diff', '0')
        if show_diff == '1':
            context['show_diff'] = True
        else:
            context['show_diff'] = False
        history = table.get_history()
        context['table'] = table
        context['history'] = history
        return context
        
class SearchView(TemplateView):
    template_name = 'ttt_gui/search/show.html'
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        matched = []
        for srv in Server.objects.all():
            for sch in srv.serverschema_set.all():
                for tbl in sch.databasetable_set.all():
                    string = '.'.join([str(srv.name), str(sch.name), str(tbl.name)])
                    match1 = re.search(q, string)
                    match2 = re.search(string, q)
                    if match1 is not None or match2 is not None:
                        matched.append([srv,sch,tbl])
        context['matched'] = matched
        return context

class AllGraphsView(TemplateView):
    template_name = 'ttt_gui/graphs/graphs_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(AllGraphsView, self).get_context_data(**kwargs)
        since_string = self.request.session.get('since_string')
        servers = Server.objects.all()
        databases = ServerSchema.objects.all()
        r = Rrdtool()
        r.server_graph(servers, since_string, 'full')
        r.database_graph(databases, since_string, 'full')
        context['servers'] = servers
        context['databases'] = databases
        return context        

class TopDatabasesView(TemplateView):
    template_name = 'ttt_gui/top_databases/show.html'
    
    def get_context_data(self, **kwargs):
        context = super(TopDatabasesView, self).get_context_data(**kwargs)
        request = self.request
        self.raw_tables = {}
        form = TopDatabasesForm(request.GET)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            percent = cleaned_data.get('percent')
            gbytes = cleaned_data.get('gbytes')
            days = cleaned_data.get('days')
            lim = cleaned_data.get('lim')
            if percent is None:
                percent = float('nan')
            if gbytes is None:
                gbytes = float('nan')
            if days is None:
                dt = datetime.min
            else:
                dt = datetime.now() - timedelta(days=days)
            if not math.isnan(percent):
                context['type'] = 'top_Pct'
                min_maxes = TableVolume.objects.exclude(database_name=None, 
                    table_name=None).filter(run_time__gt=dt).values('server',
                    'database_name', 'table_name').annotate(min_id=Min('id'), max_id=Max('id'))
                for t in min_maxes:
                    min_tbl = TableVolume.objects.get_or_none(id=t.get('min_id'))
                    max_tbl = TableVolume.objects.get_or_none(id=t.get('max_id'))
                    if min_tbl is None or max_tbl is None or min_tbl.deleted or max_tbl.deleted:
                        continue
                    if [min_tbl.server, min_tbl.database_name] not in self.raw_tables.keys():
                        self.raw_tables[(min_tbl.server, min_tbl.database_name)] = 0.0
                    if min_tbl.size != 0:
                        self.raw_tables[(min_tbl.server, min_tbl.database_name)] += (max_tbl.size+0.0-min_tbl.size+0.0)/min_tbl.size+0.0
                    raw_array = [[k, v] for k,v in self.raw_tables.items()]
                    raw_array = filter(lambda x: x[1] > percent, raw_array)
                    raw_array.sort(key=lambda x: -x[1])
                    if lim is not None:
                        raw_array = raw_array[:lim]
                    context['databases'] = raw_array
            elif not math.isnan(gbytes):
                context['type'] = 'top_GB'
                min_maxes = TableVolume.objects.exclude(database_name=None, 
                    table_name=None).filter(run_time__gt=dt).values('server',
                    'database_name', 'table_name').annotate(min_id=Min('id'), max_id=Max('id'))
                for t in min_maxes:
                    min_tbl = TableVolume.objects.get_or_none(id=t.get('min_id'))
                    max_tbl = TableVolume.objects.get_or_none(id=t.get('max_id'))
                    if min_tbl is None or max_tbl is None or min_tbl.deleted or max_tbl.deleted:
                        continue
                    if [min_tbl.server, min_tbl.database_name] not in self.raw_tables.keys():
                        self.raw_tables[(min_tbl.server, min_tbl.database_name)] = 0.0
                    self.raw_tables[(min_tbl.server, min_tbl.database_name)] += (max_tbl.size+0.0-min_tbl.size+0.0)
                    raw_array = [[k, v] for k,v in self.raw_tables.items()]
                    raw_array = filter(lambda x: x[1] > gbytes*(1024**3), raw_array)
                    raw_array.sort(key=lambda x: -x[1])
                    if lim is not None:
                        raw_array = raw_array[:lim]
                    context['databases'] = raw_array
        else:
            context['databases'] = []
        context['form'] = TopDatabasesForm()
        return context
        
class TopTablesView(TemplateView):
    template_name = 'ttt_gui/top_tables/show.html'
    
    def get_context_data(self, **kwargs):
        context = super(TopTablesView, self).get_context_data(**kwargs)
        request = self.request
        s_id = self.kwargs.get('s_id')
        d_id = self.kwargs.get('d_id')
        srv = Server.objects.get_or_none(id=s_id)
        db = ServerSchema.objects.get_or_none(id=d_id)
        context['server'] = srv
        context['database'] = db
        form = TopTablesForm(request.GET)
        valid = form.is_valid()
        cleaned_data = form.cleaned_data
        lim = cleaned_data.get('limit')
        days = cleaned_data.get('days')
        percent = cleaned_data.get('percent')
        if percent is None:
            percent = float('nan')
        if days is None:
            dt = datetime.min
        else:
            dt = datetime.now() - timedelta(days=days)
        if not valid:
            context['type'] = 'top_N'
            if s_id is None:
                tables = DatabaseTable.objects.all().order_by('-cached_size')
            else:
                if d_id is None:
                    tables = DatabaseTable.objects.filter(schema__server__id=s_id).order_by('-cached_size')
                else:
                    tables = DatabaseTable.objects.filter(schema__id=d_id, schema__server__id=s_id).order_by('-cached_size')
            if lim is not None and lim != 0:
                tables = tables[:lim]
            context['tables'] = tables
        else:
            if days != 0 and not math.isnan(percent):
                context['type'] = 'top_Pct'
                self.raw_tables = {}
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
                        self.raw_tables[(min_tbl.server, min_tbl.database_name, min_tbl.table_name)] = (max_tbl.size+0.0-min_tbl.size+0.0)/min_tbl.size+0.0
                    raw_array = [[k, v] for k,v in self.raw_tables.items()]
                    raw_array = filter(lambda x: x[1] > percent, raw_array)
                    raw_array.sort(key=lambda x: -x[1])
                    if lim is not None:
                        raw_array = raw_array[:lim]
                    context['tables'] = raw_array
            if days == 0 and limit == 0 and percent == 0:
                context['tables'] = []
        context['form'] = TopTablesForm()
        return context
