# coding=UTF8
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'renjian_neighbour.core.views.indexRequest'),
    (r'^neighbourhood/$', 'renjian_neighbour.core.views.neighbourhood'),
    (r'^users/$', 'renjian_neighbour.core.views.users'),
    (r'^error/$', 'renjian_neighbour.core.views.error'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/arthur/workspace/renjian-neighbour/renjian_neighbour/core/media/css'}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/arthur/workspace/renjian-neighbour/renjian_neighbour/core/media/js'}),
#        (r'^(?P<path>.*)$', 'django.views.static.serve',
#            {'document_root': '/home/arthur/workspace/renjian-neighbour/renjian_neighbour/core/media'}),
    )