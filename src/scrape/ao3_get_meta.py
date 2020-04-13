#!/usr/bin/env python3
"""Scraping tool to get meta information from a given fandom.

Set config options such as the time delay for each http request in config.py

Output is in csv format:
        header = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
            'category', 'status', 'fandom', 'relationship', 'character',
            'additional tags','summary', 'language', 'words', 'chapters',
            'collections','comments', 'kudos', 'bookmarks', 'hits',
            'series_part', 'series_name', 'updated', 'scrape_date']

Example URL to be scraped:
    https://archiveofourown.org/tags/Harry%20Potter%20-%20J*d*%20K*d*%20Rowling/works

Example:

    scrap.ao3_get_kudos(fandom, csv_out='meta', from_the_top=True)

TODO:

"""

import time
import datetime
import os
import csv
import sys
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from pathvalidate import replace_symbol
from unidecode import unidecode
import config as cfg
import logging


DELAY = cfg.DELAY
RAW_PATH = cfg.RAW_PATH
HTTP_HEAD = cfg.HTTP_HEADERS
MAX_ERRORS = cfg.MAX_ERRORS


def get_tag_info(category, meta):
    """ Find relationships, characters, and freeforms tags."""
    try:
        tag_list = meta.find_all("li", class_=str(category))
    except AttributeError:
        return []
    return [unidecode(result.text) for result in tag_list]


def get_stats(work):
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


def get_tags(meta):
    """Find relationships, characters, and freeforms tags"""

    tags = ['relationships', 'characters', 'freeforms']
    return list(map(lambda tag: get_tag_info(tag, meta), tags))


def get_required_tags(work):
    """Finds required tags."""

    req_tags = work.find(class_='required-tags').find_all('a')
    return [x.text for x in req_tags]


def get_header(work):
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


def get_fandoms(work):
    """ Find the list of fandoms."""

    fandoms = ''
    try:
        tag_list = work.find('h5', class_='fandoms heading').find_all('a')
        fan_list = [x.text for x in tag_list]
        fandoms = ", ".join(fan_list)
    except AttributeError:
        return []

    return [fandoms]


def get_summary(work):
    """ Find summary description and return as list of strings. """

    try:
        summary_string = work.find('blockquote', class_='userstuff summary')
        summary = summary_string.text.strip().replace('\n', ' ')
    except AttributeError:
        summary = ""
    return [summary]


def get_updated(work):
    """ Find update date. Return as list of strings. """

    try:
        date = work.find('p', class_='datetime').text
    except AttributeError:
        date = ""
    return [date]


def get_series(work):
    """ Find series info and return as list. """

    try:
        series = work.find('ul', class_='series')
        part = series.find('strong').text
        s_name = series.find('a').text
    except AttributeError:
        part, s_name = "", ""
    return [part, s_name]


def scrape_work(work, scrape_date):
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


def get_soup(base_url, i):
    """ Scrape the page, returning success and soup."""

    cur_url = base_url+str(i)
    req = requests.get(cur_url, headers=HTTP_HEAD)
    if req.status_code == 200:
        src = req.text
        soup = BeautifulSoup(src, 'html.parser')
        return soup
    else:
        raise Exception("Page not found.")


def write_works(fandom, writer, start_page=1):
    """ Write meta information for each fandom as one row in the csv. """

    scrape_date = datetime.datetime.now().strftime("%Y%b%d")
    base_url = 'https://archiveofourown.org/tags/'+quote(fandom)+'/works?page='
    logging.info(f"Base url to scrape: {base_url}")

    try:
        soup = get_soup(base_url, start_page)
        logging.info(f'PAGE: {start_page}')
    except Exception:
        logging.error(f"Unable to load {base_url+str(start_page)}")
        logging.info(f'Logged through page: {start_page}')
        return

    max_pages = int(soup.find('li', class_='next').find_previous('li').text)
    errors = 0

    while start_page < max_pages+1:
        time.sleep(DELAY)
        works = soup.find_all(class_="work blurb group")
        for work in works:
            row = scrape_work(work, scrape_date)
            try:
                writer.writerow(row)
            except csv.Error:
                error_msg = 'Unexpected error writing to csv: ' + \
                    start_page+[sys.exc_info()[0]]
                logging.error(error_msg)
        start_page += 1
        try:
            soup = get_soup(base_url, start_page)
            logging.info(f'PAGE: {start_page}')
        except Exception:
            logging.error(f"Unable to load {base_url+start_page}")
            start_page -= 1
            errors += 1
            if errors > MAX_ERRORS:
                logging.info(f'Logged through page: {start_page}')
                return
            else:
                logging.error(f"Error attempts: {errors}")
    logging.info(f'Logged through page: {start_page}')


def init_path(fandom):
    ''' Initialize data paths creating directories as needed'''

    fandom_dir = replace_symbol(fandom)
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), RAW_PATH+fandom_dir)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    os.chdir(data_path)


def find_last_page(csv_out):
    ''' Parse log file to find last page scraped '''

    page = 1
 
    with open(csv_out+'.log', 'w') as f_log:
        found = False
        count = -1
        while not found:
            line = f_log.readlines()[count]
            if 'Scraping complete' in line:
                logging.info('No new pages to scrape')
                return
            if 'PAGE:' in line:
                page = int(line.split()[2])
                logging.debug('')
                return page
            count -= 1


def scrape(fandom, csv_out='meta', from_the_top=True):
    """Initialize and commence scraping."""

    init_path(fandom)
    # check to see if the file is empty
    try:
        empty = (os.path.getsize(csv_out+'.csv') == 0)
    except OSError:
        empty = True

    # Start from the top
    if from_the_top or empty:
        with open(csv_out+'.csv', 'w') as f_out:
            logging.basicConfig(filename=csv_out+'.log',
                                filemode='w',
                                format='%(asctime)s-%(levelname)s-%(message)s',
                                level=logging.INFO)
            writer = csv.writer(f_out)
            logging.info('Writing a header row for the csv.')
            header = ['work_id', 'title', 'author', 'gifted', 'rating',
                      'warnings', 'category', 'status', 'fandom',
                      'relationship', 'character', 'additional tags',
                      'summary', 'language', 'words', 'chapters',
                      'collections', 'comments', 'kudos', 'bookmarks', 'hits',
                      'series_part', 'series_name', 'updated', 'scrape_date']
            writer.writerow(header)
            write_works(fandom, writer, start_page=1)
            logging.info('Scraping complete.')
    # Find out where we left of at
    else:
        try:
            page = find_last_page(csv_out)
            msg = f"Restarting with {page}"
            error_flag = False
        except FileNotFoundError:
            error_flag = True
            msg = "Can't find log file. Has fandom been scraped previously?"
        except IndexError:
            error_flag = True
            msg = "Unable to find last page to start scraping."
        except Exception as e:
            error_flag = True
            msg = e
        logging.basicConfig(filename=csv_out+'.log',
                            filemode='a',
                            format='%(asctime)s-%(levelname)s-%(message)s',
                            level=logging.INFO)
        if error_flag:
            logging.error(msg)
            return
        with open(csv_out+'.csv', 'a') as f_out:
            writer = csv.writer(f_out)
            write_works(fandom, writer, start_page=page)
            logging.info('Scraping complete.')
