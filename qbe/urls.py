from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', 'qbeapp.views.index', name='index'),   
    url(r'^report/$', 'qbeapp.views.get_report', name='report'),     
    url(r'^report/chart/$', 'qbeapp.views.show_report_chart', name='chart'), 
    url(r'^report/hist/(?P<hist_id>\w+\.\w+)$', 'qbeapp.views.show_histogram', name='hist'), 
    url(r'^report/(?P<page>\d+)/$', 'qbeapp.views.get_report', name='report_pgn'), 
    url(r'^db/(?P<db_key>\w+)/$', 'qbeapp.views.change_db', name='change_db'), 
    url(r'^draw/$', 'qbeapp.views.draw_graph', name='draw_graph'), 
    url(r'^export/$', 'qbeapp.views.export_csv', name='export'),
)
