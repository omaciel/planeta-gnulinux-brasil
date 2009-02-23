from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from planeta.models import Post

class RssFeed(Feed):
    title = "Planeta GNU/Linux Brasil RSS Feed"
    link = "/"
    description = "Newsfeed for Planeta GNU/Linux Brasil"

    def items(self):
        return Post.objects.order_by('-date_modified')[:10]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description
