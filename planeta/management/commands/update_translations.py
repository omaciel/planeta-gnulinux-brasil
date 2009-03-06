#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management import BaseCommand
from django.core.management.commands import compilemessages, makemessages

class Command(BaseCommand):
    help = 'Updates translation files.'
    args = 'LOCALE'

    option_list = BaseCommand.option_list + (
        make_option(
            '--locale',
            action='store_true',
            dest='locale',
            default=False,
            help='Generate and compile translation files for given locale.',
        ),
    )

    output_transaction = False

    def handle(self, _locale, **kwargs):
        extensions=['*.py', '*.html']

        if not _locale:
            print "Generating translation files for all available locales."
            makemessages.make_messages(all=True, verbosity=2, extensions=extensions)
            compilemessages.compile_messages()
        else:
            try:
                print "Generating translation files for %s" % _locale
                makemessages.make_messages(locale=locale, all=False, verbosity=2, extensions=extensions)
                compilemessages.compile_messages(locale=locale)
            except Exception, e:
                print "There was an error generating translation files for %s" % locale
