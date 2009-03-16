# -*- coding: utf-8 -*-

import os

PROJECT_DIR = os.path.dirname(__file__)

PLANET_NAME = "Sans Planet"
PLANET_URL = "http://sansplanet.gnulinuxbrasil.org"

ADMINS = (
    ('Admin', 'admin@example.com'),
)

# Make sure to change this to match your site's name
ROOT_URLCONF = 'sansplanet.urls'

# If you can't use PostgreSQL :-/, here is the MySQL configuration:
#
# DATABASE_HOST = '/var/run/mysqld/mysqld.sock'
#
# DATABASE_OPTIONS = {
#    'read_default_file': '/etc/mysql/my.cnf',
#    'init_command': 'SET storage_engine=INNODB'
# }
#·
# Please refer to the README file to create an UTF-8 database with MySQL.

DATABASE_ENGINE   = '' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME     = '' # Or path to database file if using sqlite3.
DATABASE_USER     = '' # Not used with sqlite3.
DATABASE_PASSWORD = '' # Not used with sqlite3.
DATABASE_HOST     = '' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT     = '' # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', u'American English'),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# How many articles to display on thw frontpage
PAGINATE_BY = 10

# Default media storage for avatars
AVATAR_LOCATION = 'gotchi'
# Default avatar for authors
AUTHOR_AVATAR = os.path.join(AVATAR_LOCATION, 'default.png')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'
