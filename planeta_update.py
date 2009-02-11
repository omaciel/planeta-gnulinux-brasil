#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import optparse
import datetime
import traceback
import sys

import feedparser


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
        print feed

if __name__ == '__main__':
    main()
