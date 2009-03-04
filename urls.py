from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.list_detail import object_list, object_detail
from django.conf import settings
import os

admin.autodiscover()

from planeta.models import Post
from planeta.feeds import RssFeed, AtomFeed

feeds = {
    'rss': RssFeed,
    'atom': AtomFeed,
}

post = {'queryset': Post.objects.all()}
page = {'queryset': Post.objects.all(),
        # TODO put the paginated_by value in the settings file (maybe a configuration file?)
        'paginate_by': settings.PAGINATE_BY,
        'template_name': 'planeta/index.html',
        }

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
    url(r'^$', object_list, page),
    url(r'^page/(?P<page>[0-9]+)/$', object_list, page),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name='media'),
        url(r'^gotchi/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "gotchi")}),
    )
