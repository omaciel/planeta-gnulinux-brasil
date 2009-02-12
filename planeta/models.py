from django.db import models

# Create your models here.

class Author(models.Model):
    author_name = models.CharField(max_length=50, blank=True)
    author_email = models.EmailField(blank=True)
    gotchi = models.ImageField(null=True, upload_to='gotchi',
        help_text="URL to an image file (.jpg, .png, ...) of a hackergotchi")

    def __unicode__(self):
        return u'%s' % self.author_name

class Feed(models.Model):
    author = models.ForeignKey(Author, null=False, blank=False)
    feed_title = models.CharField(max_length=200, blank=True)
    feed_url = models.URLField(unique=True)

    is_active = models.BooleanField(default=True,
        help_text='If disabled, this feed will not be further updated.')

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(max_length=50, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'feed'
        verbose_name_plural = 'feeds'
        ordering = ('feed_title', 'feed_url',)

    def __unicode__(self):
        return u'%s (%s)' % (self.feed_title, self.author.author_name)

    def save(self):
        super(Feed, self).save()

class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name='feed', null=False, blank=False)
    title = models.CharField(max_length=255)
    link = models.URLField()
    content = models.TextField(blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    guid = models.CharField(max_length=200, db_index=True)
    comments = models.URLField(blank=True)
    #tags = models.ManyToManyField(Tag, verbose_name=_('tags'))
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-date_modified',)
        unique_together = (('feed', 'guid'),)

    def __unicode__(self):
        return self.title

    def save(self):
        super(Post, self).save()

    def get_absolute_url(self):
        return self.link
