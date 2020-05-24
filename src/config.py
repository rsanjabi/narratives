#!/usr/bin/env python3
""" Module-wide constants"""


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Wait time between AO3 requests in seconds
DELAY = 5

# Location of raw data dumps. Fandom subdirectories will be located here
META_PATH = '../data/meta/'
KUDO_PATH = '../data/kudos/'
FANDOM_PATH = '../data/fandoms/'

DATA_PATH = '../data/'

MODEL_PATH = '../models/'

TBD_PREFIX = 'tbdeleted'
PROGRESS_TRACK = '.state'
INDICES_PREFIX = 'indices'
MODEL_PREFIX = 'implicit'
KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'

TXT_SUFFIX = '.txt'
LOG_SUFFIX = '.log'
DATA_SUFFIX = '.json'
PICKLE_SUFFIX = '.pkl'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

TEST_FANDOM_LIST = ["Star Wars Prequel Trilogy"]

# How many attempts at requesting page before quitting
MAX_ERRORS = 3

HOST = 'ec2-52-23-14-156.compute-1.amazonaws.com'

META_COLS = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
             'category', 'status', 'fandom', 'relationship', 'characters',
             'freeforms', 'summary', 'language', 'words', 'chapters',
             'collections', 'comments', 'kudos', 'bookmarks', 'hits',
             'series_part', 'series_name', 'updated', 'scrape_date']

SCR_WINDOW = 21          # window for number of days before we rescrape kudos

FANDOM_PAGES = ['https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms',
                'https://archiveofourown.org/media/Books%20*a*%20Literature/fandoms',
                'https://archiveofourown.org/media/Cartoons%20*a*%20Comics%20*a*%20Graphic%20Novels/fandoms',
                'https://archiveofourown.org/media/Celebrities%20*a*%20Real%20People/fandoms',
                'https://archiveofourown.org/media/Movies/fandoms',
                'https://archiveofourown.org/media/Music%20*a*%20Bands/fandoms',
                'https://archiveofourown.org/media/Other%20Media/fandoms',
                'https://archiveofourown.org/media/Theater/fandoms',
                'https://archiveofourown.org/media/TV%20Shows/fandoms',
                'https://archiveofourown.org/media/Video%20Games/fandoms']
