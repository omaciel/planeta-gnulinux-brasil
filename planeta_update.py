#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import optparse
import datetime
import traceback
import sys

import feedparser
import settings

USER_AGENT = 'sansplanet'

def process_feed(feed):

    try:
        pf = feedparser.parse(feed.feed_url, agent=USER_AGENT)
    except:
        return None

    if feed.etag == pf.etag or pf.status == 304:
        print "Feed has not changed since we last checked."
        return None

    if pf.status >= 400:
        print "There was an error parsing this feed."
        return None

    # the feed has changed (or it is the first time we parse it)
    # saving the etag and last_modified fields
    feed.etag = pf.get('etag', '')
    # some times this is None (it never should) *sigh*
    if feed.etag is None:
        feed.etag = ''

    if len(pf.entries) > 0:
        try:
            feed.last_modified = datetime.datetime.fromtimestamp(time.mktime(pf.modified))
        except:
            feed.last_modified = None

        feed.feed_title = pf.feed.get('title', '')
        feed.tagline = pf.feed.get('tagline', '')
        feed.feed_url = pf.feed.get('link', '')
        feed.last_checked = datetime.datetime.now()

        print "Feed updated"
        feed.save()

    #process_entries(feed, pf)

def process_entries(pp, posts):

    for entry in posts.get('entries', []):
        guid = entry.get('id', '')

        try:
            link = entry.get('link')
        except AttributeError:
            link = posts.link
        try:
            title = entry.get('title')
        except AttributeError:
            title = link

        if entry.has_key('author_detail'):
            author = entry.author_detail.get('name', '')
            author_email = entry.author_detail.get('email', '')
        else:
            author, author_email = '', ''

        if not author:
            author = entry.get('author', entry.get('creator', ''))
        if not author_email:
            # this should be optional~
            author_email = 'nospam@nospam.com'

        try:
            content = entry.content[0].value
        except:
            content = entry.get('summary',
                entry.get('description', ''))

        if entry.has_key('modified_parsed'):
            date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
        else:
            date_modified = None

        #fcat = self.get_tags()
        comments = entry.get('comments', '')

        from planeta.models import Post
        try:
            post = Post.objects.filter(feed=pp.id).filter(guid__in=guid)
        except:
            print "Creating new post."
            post = Post(
                feed=pp,
                title=title,
                link=link,
                content=content,
                date_modified=date_modified,
                guid=guid,
                comments=comments
            )

            post.save()

def main():
    parser = optparse.OptionParser(usage='Foo [options]')

    parser.add_option('--settings')
    options = parser.parse_args()[0]

    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings


    from planeta.models import Feed
    feeds = Feed.objects.all()

    for feed in feeds:
        #TODO: parsing code
        posts = process_feed(feed)

if __name__ == '__main__':
    main()
