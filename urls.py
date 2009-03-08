from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.date_based import archive_year
from django.conf import settings
import os

admin.autodiscover()

from planeta.models import Post
from planeta.feeds import RssFeed, AtomFeed

feeds = {
    'rss': RssFeed,
    'atom': AtomFeed,
}

posts = {'queryset': Post.objects.all()}
post = {'queryset': Post.objects.all(),
        'template_name': 'planeta/single_article.html',
}

page = {'queryset': Post.objects.all(),
        # TODO put the paginated_by value in the settings file (maybe a configuration file?)
        'paginate_by': settings.PAGINATE_BY,
        'template_name': 'planeta/index.html',
}

archive_dict = {'queryset': Post.objects.all(),
        'date_field': 'date_modified',
        'make_object_list': True,
        'template_name': 'planeta/archives.html',
}

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^post/$', object_list, posts, name='posts'),
    url(r'^post/(?P<object_id>\d+)/$', object_detail, post, name='post'),
    url(r'^$', object_list, page),
    url(r'^page/(?P<page>[0-9]+)/$', object_list, page),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^archives/(?P<year>\d{4})/$', archive_year, archive_dict, name='archives'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name='media'),
        url(r'^gotchi/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "gotchi")}),
    )
