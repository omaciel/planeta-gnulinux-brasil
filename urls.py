from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.list_detail import object_list, object_detail

admin.autodiscover()

from planeta.models import Post

post = {'queryset': Post.objects.all()}

urlpatterns = patterns('',
    # Example:
    # (r'^aggregator/', include('aggregator.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/(.*)', admin.site.root),
    url(r'^post/$', object_list, post, name='posts'),
    url(r'^post/(?P<object_id>\d+)/$', object_detail, post, name='post'),
    #(r'^artigo/(?P<post_id>\d+)/$', 'planeta.views.post'),
)
