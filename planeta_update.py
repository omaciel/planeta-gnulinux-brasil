#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import optparse
import datetime
import traceback
import sys

import feedparser

USER_AGENT = 'sansplanet'

def process_feed(feed):

    try:
        pf = feedparser.parse(feed.feed_url, agent=USER_AGENT)
    except:
        return feed

    if feed.etag == pf.etag or pf.status == 304:
        print "Feed has not changed since we last checked."
        return feed

    if pf.status >= 400:
        print "There was an error parsing this feed."
        return feed

    # the feed has changed (or it is the first time we parse it)
    # saving the etag and last_modified fields
    feed.etag = pf.get('etag', '')
    # some times this is None (it never should) *sigh*
    if feed.etag is None:
        feed.etag = ''

    try:
        feed.last_modified = mtime(pf.modified)
    except:
        pass

    feed.feed_title = pf.feed.get('title', '')
    feed.tagline = pf.feed.get('tagline', '')
    feed.feed_url = pf.feed.get('link', '')
    feed.last_checked = datetime.datetime.now()

    print "Feed updated"
    feed.save()

    process_entries(pf)

def process_entries(feed):

    import epdb; epdb.st()
    for entry in feed.entries:
        guid = entry.get('id', title)

        try:
            link = entry.link
        except AttributeError:
            link = feed.link
        try:
            title = entry.title
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

        try:
            post = models.Post.objects.filter(feed=feed.id).filter(guid__in=guid)
        except:
            print "Creating new post."
            post = models.Post(
                feed=feed,
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

    from planeta import models

    feeds = models.Feed.objects.all()

    for feed in feeds:
        #TODO: parsing code
        process_feed(feed)

if __name__ == '__main__':
    main()
