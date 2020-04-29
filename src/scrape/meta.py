#!/usr/bin/env python3
"""Scraping tool to get meta information from a given fandom.

Set config options such as the time cfg.DELAY for each http request
in config.py

Output is in csv format:
        header = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
            'category', 'status', 'fandom', 'relationship', 'character',
            'additional tags','summary', 'language', 'words', 'chapters',
            'collections','comments', 'kudos', 'bookmarks', 'hits',
            'series_part', 'series_name', 'updated', 'scrape_date']

Example URL to be scraped:
    https://archiveofourown.org/tags/Harry%20Potter%20-%20J*d*%20K*d*%20Rowling/works

Example:

    scrap.kudos(fandom, from_the_top=True)

TODO:
    * Need to add proper logging functionality and
        from_the_top=False accurately

"""

import time
import datetime
import os
import csv
import sys
from typing import List, Any
import logging
from logging import Logger

from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

import utils.paths as paths
import config as cfg


def get_tag_info(category: str, meta: BeautifulSoup) -> List[str]:
    """ Find relationships, characters, and freeforms tags."""
    try:
        tag_list = meta.find_all("li", class_=category)
    except AttributeError:
        return []
    return [unidecode(result.text) for result in tag_list]


def get_stats(work: BeautifulSoup) -> List[str]:
    """
    Find stats (language, published, status, date status, words, chapters,
    comments, kudos, bookmarks, hits
    """

    categories = ['language', 'words', 'chapters', 'collections', 'comments',
                  'kudos', 'bookmarks', 'hits']
    stats = []
    for cat in categories:
        try:
            result = work.find("dd", class_=cat).text
        except AttributeError:
            result = ""
        stats.append(result)
    return stats


def get_tags(meta: BeautifulSoup) -> Any:
    """Find relationships, characters, and freeforms tags"""

    tags = ['relationships', 'characters', 'freeforms']
    return list(map(lambda tag: get_tag_info(tag, meta), tags))


def get_required_tags(work: BeautifulSoup) -> List[str]:
    """Finds required tags."""

    req_tags = work.find(class_='required-tags').find_all('a')
    return [x.text for x in req_tags]


def get_header(work: BeautifulSoup) -> List[str]:
    """Finds header information (work_id, title, author, gifted to user)."""

    result = work.find('h4', class_='heading').find_all('a')
    work_id = result[0].get('href').strip('/works/')
    title = result[0].text

    auth_list = []
    header_text = work.find('h4', class_='heading').text
    if "Anonymous" in header_text:
        auth = "Anonymous"
    else:
        authors = work.find_all('a', rel='author')
        for author in authors:
            auth_list.append(author.text)
        auth_str = str(auth_list)
        auth = auth_str.replace('[', '').replace(']', '').replace("'", '')

    gift_list = []
    for link in result:
        href = link.get('href')
        if 'gifts' in href:
            gift_list.append(link.text)

    if len(gift_list) == 0:
        gift = ""
    else:
        gift_str = str(gift_list)
        gift = gift_str.replace('[', '').replace(']', '').replace("'", '')

    return [work_id, title, auth, gift]


def get_fandoms(work: BeautifulSoup) -> List[str]:
    """ Find the list of fandoms."""

    fandoms = ''
    try:
        tag_list = work.find('h5', class_='fandoms heading').find_all('a')
        fan_list = [x.text for x in tag_list]
        fandoms = ", ".join(fan_list)
    except AttributeError:
        return []

    return [fandoms]


def get_summary(work: BeautifulSoup) -> List[str]:
    """ Find summary description and return as list of strings. """

    try:
        summary_string = work.find('blockquote', class_='userstuff summary')
        summary = summary_string.text.strip().replace('\n', ' ')
    except AttributeError:
        summary = ""
    return [summary]


def get_updated(work: BeautifulSoup) -> List[str]:
    """ Find update date. Return as list of strings. """

    try:
        date = work.find('p', class_='datetime').text
    except AttributeError:
        date = ""
    return [date]


def get_series(work: BeautifulSoup) -> List[str]:
    """ Find series info and return as list. """

    try:
        series = work.find('ul', class_='series')
        part = series.find('strong').text
        s_name = series.find('a').text
    except AttributeError:
        part, s_name = "", ""
    return [part, s_name]


def scrape_work(work: BeautifulSoup, scrape_date: str) -> List[str]:
    """ Find each HTML element and parse out the details into a row. """

    tags = get_tags(work)
    req_tags = get_required_tags(work)
    stats = get_stats(work)
    header_tags = get_header(work)
    fandoms = get_fandoms(work)
    summary = get_summary(work)
    updated = get_updated(work)
    series = get_series(work)
    row = header_tags + req_tags + fandoms + \
        list(map(lambda x: ', '.join(x), tags)) + summary + stats + series + \
        updated + [scrape_date]
    return row


def get_soup(base_url: str, i: int) -> BeautifulSoup:
    """ Scrape the page, returning success and soup."""

    cur_url = base_url+str(i)
    req = requests.get(cur_url, headers=cfg.HTTP_HEADERS)
    if req.status_code == 200:
        src = req.text
        soup = BeautifulSoup(src, 'html.parser')
        return soup
    else:
        raise Exception("Page not found.")


def write_works(fandom: str, writer: Any,
                logger: Logger, start_page: int = 1) -> None:
    """ Write meta information for each fandom as one row in the csv. """

    scrape_date = datetime.datetime.now().strftime("%Y%b%d")
    base_url = 'https://archiveofourown.org/tags/'+quote(fandom)+'/works?page='
    logger.info(f"Base url to scrape: {base_url}")

    try:
        soup = get_soup(base_url, start_page)
        logger.info(f'PAGE: {start_page}')
    except Exception:
        logger.exception(f"Exception occurred:")
        logger.error(f"Unable to load {base_url+str(start_page)}")
        logger.info(f'Logged through page: {start_page}')
        return

    try:
        next_element = soup.find('li', class_='next')
        max_pages = int(next_element.find_previous('li').text)
    except AttributeError:
        max_pages = 1

    errors = 0

    while start_page < max_pages+1:
        time.sleep(cfg.DELAY)
        works = soup.find_all(class_="work blurb group")
        for work in works:
            row = scrape_work(work, scrape_date)
            try:
                writer.writerow(row)
            except csv.Error:
                error_msg = 'Unexpected error writing to csv: ' + \
                    str(start_page)+str(sys.exc_info()[0])
                logger.error(error_msg)
        start_page += 1
        try:
            soup = get_soup(base_url, start_page)
            logger.info(f'PAGE: {start_page}')
        except Exception:
            logger.error(f"Unable to load {base_url+str(start_page)}")
            start_page -= 1
            errors += 1
            if errors > cfg.MAX_ERRORS:
                err = f'Max errors ({cfg.MAX_ERRORS}) reached.'
                err2 = f' Logged through page: {start_page}'
                logger.info(err+err2)
                return
            else:
                time.sleep(20*cfg.DELAY)
                logger.error(f"Error attempts: {errors} of {cfg.MAX_ERRORS}")
    logger.info(f'Logged through page: {start_page}')


def find_last_page(log_path):
    ''' Parse log file to find last page scraped '''

    page = 1
    with open(log_path, 'r') as f_log:
        found = False
        count = -1
        while not found:
            line = f_log.readlines()[count]
            if 'Scraping complete' in line:
                return -1
            if 'PAGE:' in line:
                page = int(line.split()[2])
                return page
            count -= 1
    return -1


def scrape_starting_at(fandom, meta_path, log_path, msg='',
                       page=1, from_the_top=True):

    if from_the_top:
        with open(meta_path, 'w') as f_out:
            logger = logging.getLogger(fandom+'meta')
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(log_path, mode='w')
            formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                          '%(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            writer = csv.writer(f_out)
            if msg != '':
                logger.info(msg)
            logger.info('Writing a header row for the csv.')
            header = ['work_id', 'title', 'author', 'gifted', 'rating',
                      'warnings', 'category', 'status', 'fandom',
                      'relationship', 'character', 'additional tags',
                      'summary', 'language', 'words', 'chapters',
                      'collections', 'comments', 'kudos', 'bookmarks', 'hits',
                      'series_part', 'series_name', 'updated', 'scrape_date']
            writer.writerow(header)
            write_works(fandom, writer, logger, start_page=1)
            logger.info('Scraping complete.')
            fh.close()
    else:
        with open(meta_path, 'a') as f_out:
            logger = logging.getLogger(fandom+'meta')
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(log_path, mode='a')
            formatter = logging.Formatter('%(asctime)s-%(levelname)s-' +
                                          '%(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            writer = csv.writer(f_out)
            logger.info(f'Picking up from {page}')
            write_works(fandom, writer, logger, start_page=page)
            logger.info('Scraping complete.')
            fh.close()


def scrape(fandom, from_the_top=True):
    """Initialize and error checking to determine what state scraping is in."""

    meta_path = paths.meta_path(fandom)
    log_path = paths.meta_log_path(fandom)

    if from_the_top:
        scrape_starting_at(fandom, meta_path, log_path)
        return

    # check to see if the file is empty
    try:
        output_file_missing = (os.path.getsize(meta_path) == 0)
    except OSError:
        output_file_missing = True

    # Couldn't find output file; start from the top
    if output_file_missing:
        msg = "File not found. New file created."
        scrape_starting_at(fandom, meta_path, log_path, msg)
        return

    try:
        page = find_last_page(log_path)
        # Need to add proper logging functionality
        if page == -1:
            print(f"Scraping already complete.")
            return
        msg = f"Restarting with {page}"
        scrape_starting_at(fandom, meta_path, log_path, msg,
                           page=page, from_the_top=False)
        return
    except FileNotFoundError:
        page = 1
        msg = "Can't find log file. Starting from the top."
    except IndexError:
        msg = "Unable to find last page to start scraping. \
               Starting from the top."
        page = 1
    except Exception as e:
        msg = f'Undefined error: {e}. Starting from the top.'
        page = 1

    scrape_starting_at(fandom, meta_path, log_path, msg,
                       page=page, from_the_top=True)
    return
