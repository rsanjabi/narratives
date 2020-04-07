#!/usr/bin/env python
""" Module-wide constants"""

# Wait time between AO3 requests in seconds
DELAY = 4

# File name of output file
OUTPUT_FILE = 'work_id_list.txt'

# Location of raw data dumps. Fandom subdirectories will be located here
RAW_PATH = '../../data/raw/'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent': 'Scraping meta for fan analysis; Contact rebecca.sanjabi@gmail.com'}

# When testing a single fandom
TEST_FANDOM = 'Star Wars: The Clone Wars (2008) - All Media Types'
