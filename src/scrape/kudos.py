#!/usr/bin/env python3
"""Scraping tool to get a list of kudos for a list of fanworks.

Set config options such as the time cfg.DELAY for each http
request in config.py

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
from typing import Any
from pathlib import Path

from bs4 import BeautifulSoup
import logging
from logging import Logger

import utils.paths as paths
import config as cfg


def write_kudo_to_csv(work_id: str, writer: Any, logger: Logger) -> int:
    '''
    work_id is the AO3 ID of a work
    writer is a csv writer object
    the output of this program is a row in the CSV file containing works ID and
        username who gave it kudos
    header_info should be the header info to encourage ethical scraping.
    '''

    url = 'http://archiveofourown.org/works/'+work_id+'/kudos'

    req = requests.get(url, headers=cfg.HTTP_HEADERS)
    if req.status_code != 200:
        msg1 = f"Unable to load page for word: {work_id} "
        msg2 = f'HTTP status code: {req.status_code}'
        logger.error(msg1 + msg2)
        return 1

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
            return 1
    logger.info(f'Scraped {len(kudo_list)} kudos for ID: {work_id}')
    return 0


def find_last_work(kudos_file: Path) -> str:
    ''' Parse log file to find work_id's kudos scraped '''

    with open(kudos_file, 'r') as f_file:
        last_line = f_file.readlines()[-1]
        work_id = last_line.split()[0]
        return work_id


def scrape_starting_at(fandom: str, meta_path: Path, kudos_path: Path,
                       log_path: Path, msg: str = '', work: str = '',
                       from_the_top: bool = False):
    ''' if from_the_top = False then work should be equal to fan id. If work
        is equal to a fan ID from_the_top should be True '''
    errors = 0

    if from_the_top:

        # Set up logger
        logger = logging.getLogger(fandom+'kudos')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path, mode='w')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                      '%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Create or write over outputfile
        with open(kudos_path, 'w') as f_out:
            writer = csv.writer(f_out)

            # First a header row
            header = ['work_id', 'user']
            writer.writerow(header)
            try:
                # Open input file
                with open(meta_path, 'r') as f_in:
                    reader = csv.reader(f_in)
                    for i, row in enumerate(reader):
                        # Skip header row
                        if i == 0:
                            continue
                        errors += write_kudo_to_csv(row[0], writer, logger)
                        if errors > cfg.MAX_ERRORS:
                            logger.error(f"Exceeded max page loading errors.")
                            break
                        time.sleep(cfg.DELAY)
            except FileNotFoundError as e:
                logger.error(f"Meta file missing exception: {e}")

    # Find out where we left off at and append
    else:
        # Set up logger
        logger = logging.getLogger(fandom+'kudos')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                      '%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # Open and append to output file
        with open(kudos_path, 'a') as f_out:
            writer = csv.writer(f_out)
            # Open input file
            with open(meta_path, 'r+') as f_in:
                reader = csv.reader(f_in)
                encountered = False
                for row in reader:
                    # Write out rows again once we've encountered the work
                    if encountered:
                        errors += write_kudo_to_csv(row[0], writer, logger)
                        if errors > cfg.MAX_ERRORS:
                            logger.error(f"Exceeded max page loading errors.")
                            break
                        time.sleep(cfg.DELAY)
                    # Is this the last work we scraped?
                    elif row[0] == work.split(',')[0]:
                        encountered = True

    logger.info('Scraping complete.')


def scrape(fandom: str, from_the_top: bool = False) -> None:
    """ Scrape the kudos from a list of fanwork_ids """

    meta_path = paths.meta_path(fandom)
    log_path = paths.kudo_log_path(fandom)
    kudos_path = paths.kudo_path(fandom)

    if from_the_top:
        scrape_starting_at(fandom, meta_path, kudos_path, log_path,
                           msg=fandom, from_the_top=True)
        return

    # check to see if the file is empty
    try:
        output_file_missing = (os.path.getsize(kudos_path) == 0)
    except OSError:
        output_file_missing = True

    if output_file_missing:
        msg = "File not found. New file created."
        scrape_starting_at(fandom, meta_path, kudos_path, log_path,
                           msg=msg, from_the_top=True)
        return

    try:
        last_work = find_last_work(kudos_path)
        msg = f"Restarting from work {last_work}"
        scrape_starting_at(fandom, meta_path, kudos_path, log_path,
                           msg=msg, work=last_work,
                           from_the_top=False)
    except Exception as e:
        msg = f'Undefined error: {e}. Starting from the top.'
        return
    return
