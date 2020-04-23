#!/usr/bin/env python3
""" Module-wide constants"""

# Wait time between AO3 requests in seconds
DELAY = 5

# Location of raw data dumps. Fandom subdirectories will be located here
DATA_PATH = '../data/raw/'
MODEL_PATH = '../models/'

INDICES_PREFIX = 'indices'
MODEL_PREFIX = 'implicit'
KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'

LOG_SUFFIX = '.log'
DATA_SUFFIX = '.csv'
PICKLE_SUFFIX = '.pkl'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

# When testing a single fandom
# TEST_FANDOM = 'Star Wars: The Clone Wars (2008) - All Media Types'
# TEST_FANDOM = 'The Mandalorian (TV)'
# TEST_FANDOM = 'Star Wars: A New Dawn - John Jackson Miller'
# TEST_FANDOM = 'Star Wars: Kanan (Comics)'
# TEST_FANDOM = 'Star Wars: Thrawn Series - Timothy Zahn (2017)'
# TEST_FANDOM = 'Star Wars Original Trilogy'
# TEST_FANDOM = 'Rogue One: A Star Wars Story (2016)'
# TEST_FANDOM = 'Star Wars: Rebels'
# TEST_FANDOM = 'Star Wars: Resistance (Cartoon)'

# How many attempts at requesting page before quitting
MAX_ERRORS = 3
