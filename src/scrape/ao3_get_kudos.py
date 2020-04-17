#!/usr/bin/env python3
"""Scraping tool to get a list of kudos for a list of fanworks.

Set config options such as the time DELAY for each http request in config.py

Output is in csv format of <fandom_id>,<named_kudo_giver>

Input is a csv where the first field is a fandom_id.

Example URL to be scraped:

    https://archiveofourown.org/works/14927703/kudos

Example:

    scrap.ao3_get_kudos(in_csv_file, out_csv_file, restart)

TODO:
    * Do paths work?
    * Restart working?

"""

import time
import os
import csv
import requests
from bs4 import BeautifulSoup
from pathvalidate import replace_symbol
import config as cfg
import logging

DELAY = cfg.DELAY
RAW_PATH = cfg.RAW_PATH
HTTP_HEAD = cfg.HTTP_HEADERS


def init_path(fandom):
    ''' Initialize data paths creating directories as needed'''

    fandom_dir = replace_symbol(fandom)
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), RAW_PATH+fandom_dir)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    os.chdir(data_path)


def write_kudo_to_csv(work_id, writer, logger):
    '''
    work_id is the AO3 ID of a work
    writer is a csv writer object
    the output of this program is a row in the CSV file containing works ID and
        username who gave it kudos
    header_info should be the header info to encourage ethical scraping.
    '''

    url = 'http://archiveofourown.org/works/'+str(work_id)+'/kudos'

    req = requests.get(url, headers=HTTP_HEAD)
    if req.status_code != 200:
        logger.error(f'Unable to load page for: {work_id}')
        return

    src = req.text
    soup = BeautifulSoup(src, 'html.parser')

    try:
        kudo_soup = soup.find(id="kudos").find_all('a')
        # Convert to set to remove dups due to AO3 kudo errors
        kudo_list = [x.text for x in set(kudo_soup)]
    except AttributeError:
        kudo_list = []
    for kudo in kudo_list:
        row = [work_id] + [kudo]
        try:
            writer.writerow(row)
        except csv.Error:
            logger.error(f'csv.Error, skipping remaining kudos {work_id}')
            return
    logger.info(f'WORK ID: {work_id}')


def find_last_work(csv_out):
    ''' Parse log file to find work_id's kudos scraped '''

    with open(csv_out+'.csv', 'r') as f_file:
        last_line = f_file.readlines()[-1]
        work_id = last_line.split()[0]
        return work_id


def scrape_starting_at(msg='', csv_in='meta', csv_out='kudos',
                       work='', from_the_top=False):

    ''' if from_the_top = False then work should be equal to fan id. If work
        is equal to a fan ID from_the_top should be True '''

    if from_the_top:

        # Set up logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(csv_out + '.log', mode='w')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                      '%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Create or write over outputfile
        with open(csv_out+'.csv', 'w') as f_out:
            writer = csv.writer(f_out)

            # First a header row
            header = ['work_id', 'user']
            writer.writerow(header)

            # Open input file
            with open(csv_in+'.csv', 'r') as f_in:
                reader = csv.reader(f_in)
                for i, row in enumerate(reader):
                    # Skip header row
                    if i == 0:
                        continue
                    write_kudo_to_csv(row[0], writer, logger)
                    time.sleep(DELAY)

    # Find out where we left off at and append
    else:
        # Set up logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(csv_out + '.log', mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                      '%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # Open and append to output file
        with open(csv_out+'.csv', 'a') as f_out:
            writer = csv.writer(f_out)
            # Open input file
            with open(csv_in+'.csv', 'r+') as f_in:
                reader = csv.reader(f_in)
                encountered = False
                for row in reader:
                    # Write out rows again once we've encountered the work
                    if encountered:
                        write_kudo_to_csv(row[0], writer, logger)
                        time.sleep(DELAY)
                    # Is this the last work we scraped?
                    elif row[0] == work.split(',')[0]:
                        print(f'DEBUG 7 Encountered {row[0]} =={work}')
                        encountered = True

    logger.info('Scraping complete.')


def scrape(fandom, csv_in='meta', csv_out='kudos', from_the_top=False):
    """ Scrape the kudos from a list of fanwork_ids """

    init_path(fandom)

    if from_the_top:
        scrape_starting_at(fandom, csv_in, csv_out, from_the_top=True)
        return

    # check to see if the file is empty
    try:
        output_file_missing = (os.path.getsize(csv_out+'.csv') == 0)
    except OSError:
        output_file_missing = True

    if output_file_missing:
        msg = "File not found. New file created."
        scrape_starting_at(msg, csv_in, csv_out, from_the_top=True)
        return

    try:
        last_work = find_last_work(csv_out)
        msg = f"Restarting from work {last_work}"
        print(f"DEBUG 2: {last_work}")
        scrape_starting_at(msg, csv_in, csv_out, work=last_work,
                           from_the_top=False)
    except Exception as e:
        print(f"DEBUG 3 :{e}")
        msg = f'Undefined error: {e}. Starting from the top.'
        return
        # scrape_starting_at(msg, csv_in, csv_out, from_the_top=True)
    return
