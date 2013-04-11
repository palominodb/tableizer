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
