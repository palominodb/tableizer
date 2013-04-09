from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from ttt_gui import views

urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url=reverse_lazy("server_list"),), name='index'),
        
        url(r'^servers/$', views.ServerListView.as_view(), name='server_list'),
        url(r'^servers/(?P<id>\d+)/$', views.ServerDetailView.as_view(), name='server_detail'),
        
        url(r'^databases/$', views.DatabaseListView.as_view(), name='database_list'),
        url(r'^databases/top/$', views.TopDatabasesView.as_view(), name='top_databases'),
        url(r'^databases/(?P<id>\d+)/$', views.DatabaseDetailView.as_view(), name='database_detail'),
        
        url(r'^tables/(?P<id>\d+)/$', views.TableDetailView.as_view(), name='table_detail'),
        url(r'^tables/top/$', views.TopTablesView.as_view(), name='top_tables'),
        url(r'^tables/top/(?P<s_id>\d+)/$', views.TopTablesView.as_view(), name='top_tables_srv'),
        url(r'^tables/top/(?P<s_id>\d+)/(?P<d_id>\d+)/$', views.TopTablesView.as_view(), name='top_tables_srv_db'),
        
        url(r'^history/$', views.HistoryIndexView.as_view(), name='history_index'),
        url(r'^history/(?P<id>\d+)/$', views.ShowHistoryView.as_view(), name='show_history'),
        url(r'^graphs/$', views.AllGraphsView.as_view(), name='all_graphs'),
        
        url(r'^search/$', views.SearchView.as_view(), name='search'),
        
)
