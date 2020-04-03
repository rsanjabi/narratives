#!/usr/bin/env python

import argparse
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

DELAY = cfg.DELAY
RAW_PATH = cfg.RAW_PATH

def get_tag_info(category, meta):
    '''
    given a category and a 'work meta group, returns a list of tags (eg, 'rating' -> 'explicit')
    '''
    try:
        tag_list = meta.find_all("li", class_=str(category))
    except AttributeError:
        return []
    return [unidecode(result.text) for result in tag_list]

def get_stats(work):
    '''
    returns a list of
    language, published, status, date status, words, chapters, comments, kudos, bookmarks, hits
    '''
    categories = ['language', 'words', 'chapters', 'collections', 'comments',\
                     'kudos', 'bookmarks', 'hits']
    stats = []
    for cat in categories:
        try:
            result = work.find("dd", class_=cat).text
        except:
            result = ""
        stats.append(result)

    #stats[0] = stats[0].rstrip().lstrip() #language has weird whitespace characters

    return stats

def get_tags(meta):
    '''
    returns a list of lists, of
    rating, category, fandom, pairing, characters, additional_tags
    '''
    tags = ['relationships', 'characters', 'freeforms']
    return list(map(lambda tag: get_tag_info(tag, meta), tags))

def get_required_tags(work):
    req_tags = work.find(class_='required-tags').find_all('a')
    return [x.text for x in req_tags]

def get_header(work):
    '''
    returns work_id, title, author, gifted to user
    '''

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
        auth = str(auth_list).replace('[', '').replace(']', '')

    gift_list = []
    for link in result:
        href = link.get('href')
        if 'gifts' in href:
            gift_list.append(link.text)

    if len(gift_list) == 0:
        gift = ""
    else:
        gift = str(gift_list).replace('[', '').replace(']', '')

    return [work_id, title, auth, gift]


def get_fandoms(work):
    fandoms = ''
    try:
        tag_list = work.find('h5', class_='fandoms heading').find_all('a')
        fan_list = [x.text for x in tag_list]
        fandoms = ", ".join(fan_list)

    except AttributeError:
        return []

    return [fandoms]

def get_summary(work):
    try:
        summary = work.find('blockquote', class_='userstuff summary').text.strip().replace('\n', '')
    except AttributeError:
        summary = ""
    return [summary]

def get_updated(work):
    try:
        date = work.find('p', class_='datetime').text
    except AttributeError:
        date = ""
    return [date]

def get_series(work):
    try:
        series = work.find('ul', class_='series')
        part = series.find('strong').text
        s_name = series.find('a').text
    except AttributeError:
        part, s_name = "", ""
    return [part, s_name]

def scrape_work(work, scrape_date):
    tags = get_tags(work)
    req_tags = get_required_tags(work)
    stats = get_stats(work)
    header_tags = get_header(work)
    fandoms = get_fandoms(work)
    summary = get_summary(work)
    updated = get_updated(work)
    series = get_series(work)
    row = header_tags + req_tags + fandoms + \
        list(map(lambda x: ', '.join(x), tags)) + summary + stats + series + updated + [scrape_date]
    return row

def get_soup(base_url, i, headers):
    cur_url = base_url+str(i)
    print(f"Scraping page: {cur_url}")
    req = requests.get(cur_url, headers=headers)
    if req.status_code == 200:
        src = req.text
        soup = BeautifulSoup(src, 'html.parser')
        return True, soup
    else:
        return False, None

def write_fic_to_csv(fandom, writer, errorwriter, headers=''):

    scrape_date = datetime.datetime.now().strftime("%Y%b%d")
    base_url = 'https://archiveofourown.org/tags/'+quote(fandom)+'/works?page='
    page_count = 1

    print(f'Scraping: {base_url}')

    loaded, soup = get_soup(base_url, page_count, headers)

    if not loaded:
        print('Access Denied')
        error_row = [fandom] + ['Access Denied']
        errorwriter.writerow(error_row)
        return

    max_pages = int(soup.find('li', class_='next').find_previous('li').text)

    while page_count < max_pages+1 and loaded:
        works = soup.find_all(class_="work blurb group")
        for work in works:
            row = scrape_work(work, scrape_date)
            try:
                writer.writerow(row)
            except:
                print('Unexpected error: ', sys.exc_info()[0])
                #error_row = [fic_id] +  [sys.exc_info()[0]]
                #errorwriter.writerow(error_row)
        page_count += 1
        loaded, soup = get_soup(base_url, page_count, headers)


    print('Done.')

def get_args():
    '''
    TODO: Is this still useful? If so, fix headers so not a dict
    '''
    parser = argparse.ArgumentParser(description='Scrape and save some fanfic, given their AO3 IDs')
    parser.add_argument(
        'fandom', metavar='FANDOM', nargs='+',
        help='a single fandom in quotes or a csv input filename')
    parser.add_argument(
        '--csv', default='meta.csv',
        help='csv output file name')
    parser.add_argument(
        '--header', default='',
        help='user http header')
    parser.add_argument(
        '--restart', default='',
        help='work_id to start at from within a csv')
    args = parser.parse_args()
    fandom = str(args.fandom[0])
    is_csv = False      # Replace this with code to pick up a certain page number if interrupted
    csv_out = str(args.csv)
    headers = str(args.header)
    restart = str(args.restart)
    return fandom, csv_out, headers, restart, is_csv

def process_id(fic_id, restart, found):
    if found:
        return True
    if fic_id == restart:
        return True
    else:
        return False

def scrape(fandom, csv_out, headers, restart, is_csv):
    fandom_dir = replace_symbol(fandom)
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RAW_PATH+fandom_dir)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    os.chdir(data_path)
    with open(csv_out, 'a') as f_out:
        writer = csv.writer(f_out)
        with open("errors_" + csv_out, 'a') as e_out:
            errorwriter = csv.writer(e_out)
            #does the csv already exist? if not, let's write a header row.
            if os.stat(csv_out).st_size == 0:
                print('Writing a header row for the csv.')
                header = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings', 'category',
                          'status', 'fandom', 'relationship', 'character', 'additional tags',
                          'summary', 'language', 'words', 'chapters', 'collections', 'comments',
                          'kudos', 'bookmarks', 'hits', 'series_part', 'series_name', 'updated',
                          'scrape_date']
                writer.writerow(header)
            if is_csv:
                with open("errors_" + csv_out, 'r+') as f_in:
                    reader = csv.reader(f_in)
                    if restart is '':
                        for row in reader:
                            if not row:
                                continue
                            write_fic_to_csv(row[0], writer, errorwriter, headers)
                            time.sleep(DELAY)
                    else:
                        found_restart = False
                        for row in reader:
                            if not row:
                                continue
                            # TODO rewrite for restart to work restart at page??
                            found_restart = process_id(row[0], restart, found_restart)
                            if found_restart:
                                write_fic_to_csv(row[0], writer, errorwriter, headers)
                                time.sleep(DELAY)
                            else:
                                print('Skipping already processed fic')
            else:
                write_fic_to_csv(fandom, writer, errorwriter, headers)
                time.sleep(DELAY)

if __name__ == "__main__":
    fandom, csv_out, headers, restart, is_csv = get_args()
    scrape(fandom, csv_out, headers, restart, is_csv)
