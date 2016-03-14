#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sanyam Khurana'
SITENAME = u'Sanyam Khurana'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('twitter', 'https://twitter.com/ErSanyamKhurana'),
    ('github', 'https://github.com/CuriousLearner'),
    ('facebook','https://facebook.com/sanyam.khurana96'),
    ('envelope','mailto:sanyam@sanyamkhurana.com')
)

STATIC_PATHS = ['images']

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'theme/pelican-clean-blog'
SITESUBTITLE = 'Curious Learner | FOSS Contributor | Passionate Geek'

MENUITEMS = (
    ('FOSS','/category/foss.html'),
)

RELATIVE_URLS = True
