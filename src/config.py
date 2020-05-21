#!/usr/bin/env python3
""" Module-wide constants"""


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Wait time between AO3 requests in seconds
DELAY = 5

# Location of raw data dumps. Fandom subdirectories will be located here
DATA_PATH = '../data/raw/'
MODEL_PATH = '../models/'

INDICES_PREFIX = 'indices'
MODEL_PREFIX = 'implicit'
KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'
META_DB_PREFIX = 'meta_db'
KUDOS_DB_PREFIX = 'kudos_db'

LOG_SUFFIX = '.log'
DATA_SUFFIX = '.json'
PICKLE_SUFFIX = '.pkl'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

TEST_FANDOM_LIST = ["LEGO Star Wars: The Padawan Menace (Short Film)"]

# How many attempts at requesting page before quitting
MAX_ERRORS = 3

HOST = 'ec2-52-23-14-156.compute-1.amazonaws.com'

META_COLS = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
             'category', 'status', 'fandom', 'relationship', 'characters',
             'freeforms', 'summary', 'language', 'words', 'chapters',
             'collections', 'comments', 'kudos', 'bookmarks', 'hits',
             'series_part', 'series_name', 'updated', 'scrape_date']

SCR_WINDOW = 21          # window for number of days before we rescrape kudos
