#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sanyam Khurana'
SITENAME = u'Sanyam Khurana'
SITEURL = 'https://www.sanyamkhurana.com/blog'

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
    ('facebook', 'https://facebook.com/CuriousLearner'),
    ('envelope', 'mailto:sanyam@sanyamkhurana.com'),
    ('feed', 'https://www.sanyamkhurana.com/blog/feeds/all.rss.xml')
)

# STATIC_PATHS = ['images', 'extra/CNAME']
# EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'theme/clean-blog'
SITESUBTITLE = 'Curious Learner | FOSS Contributor | Passionate Geek'

# MENUITEMS = (
#     ('FOSS','blog/category/foss.html'),
# )
