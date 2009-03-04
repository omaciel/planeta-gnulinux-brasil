from django.conf import settings
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from planeta.models import Post

class RssFeed(Feed):
    title = "%s RSS Feed" % settings.PLANET_NAME
    link = "/"
    description = "Newsfeed for %s" % settings.PLANET_NAME

    def items(self):
        return Post.objects.order_by('-date_modified')[:10]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description
