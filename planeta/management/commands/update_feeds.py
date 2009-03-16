#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

import os
import time
import optparse
import datetime
import traceback
import sys

import feedparser

USER_AGENT = 'sansplanet'

def fetch_feed(feed):

    channel = None

    try:
        channel = feedparser.parse(feed.feed_url, etag=feed.etag, agent=USER_AGENT)
    except Exception, e:
        print str(e)
        pass

    return channel

def process_feed(feed):

    channel = fetch_feed(feed)

    import epdb; epdb.st()
    if feed.etag == channel.etag or channel.status == 304:
        print "Feed has not changed since we last checked."
        return None

    if channel.status >= 400:
        print "There was an error parsing this feed."
        return None

    # the feed has changed (or it is the first time we parse it)
    # saving the etag and last_modified fields
    feed.etag = channel.get('etag', '')
    # some times this is None (it never should) *sigh*
    if feed.etag is None:
        feed.etag = ''

    try:
        feed.last_modified = datetime.datetime.fromtimestamp(time.mktime(channel.modified))
    except:
        feed.last_modified = None

    feed.feed_title = channel.feed.get('title', feed.feed_title)
    #feed.tagline = channel.feed.get('tagline', feed.tagline)
    feed.site_url = channel.feed.get('link', feed.feed_url)
    feed.last_checked = datetime.datetime.now()

    print "Feed updated"
    feed.save()

    return channel

def process_entries(feed, channel):

    for entry in channel.entries:
        entry

        guid = entry.get('id', feed.feed_title)

        try:
            link = entry.link
        except AttributeError:
            link = feed.link
        try:
            title = entry.title
        except AttributeError:
            title = link

        if 'author_detail' in entry:
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

        if 'modified_parsed' in entry and entry.modified_parsed is not None:
            date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
        else:
            date_modified = datetime.datetime.now()

        #fcat = self.get_tags()
        comments = entry.get('comments', '')

        from planeta.models import Post

        post = Post.objects.filter(feed=feed.id, guid=guid)
        if not post:
            print "Creating new post."
            post = Post()
        else:
            print "Updating post"
            post = post[0]

        post.feed=feed
        post.title=title
        post.link=link
        post.content=content
        post.date_modified=date_modified
        post.guid=guid
        post.comments=comments

        post.save()

class Command(BaseCommand):
    def handle(self, **kwargs):
        from planeta.models import Feed

        feeds = Feed.objects.all()

        for feed in feeds:
            #TODO: parsing code
            channel = process_feed(feed)
            if channel:
                process_entries(feed, channel)
