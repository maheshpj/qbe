from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', 'qbeapp.views.index', name='index'),   
    url(r'^report/$', 'qbeapp.views.get_report', name='report'), 
)
