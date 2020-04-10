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
    * Remove get_args()
    * Do paths work?
    * Restart working?
    * access_denied() is a stub

"""

import time
import os
import csv
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from pathvalidate import replace_symbol
import config as cfg

DELAY = cfg.DELAY
RAW_PATH = cfg.RAW_PATH
HTTP_HEAD = cfg.HTTP_HEADERS

def get_args():
    """Converts command line arguments into variables."""

    parser = argparse.ArgumentParser(description='Scrape AO3 work IDs to find users who gave kudos')
    parser.add_argument('--fandom', default='', help='fandom name')
    parser.add_argument('--in_csv', default='meta.csv', help='csv input file name')
    parser.add_argument('--out_csv', default='kudos.csv', help='csv output file name')
    parser.add_argument('--restart', default='', help='work_id to start at from within a csv')

    args = parser.parse_args()
    fandom = str(args.fandom)
    output_file = str(args.out_csv)
    input_file = str(args.in_csv)
    restart = str(args.restart)

    return fandom, input_file, output_file, restart

def process_id(work_id, restart, found):
    """ Not found and not restart """
    if found:
        return True
    if work_id == restart:
        return True
    else:
        return False

def access_denied(soup):
    '''
    Possible tags to search for when kudos file is not found
    Stub function to add to as needed
    '''
    if soup.find(class_="flash error"):
        pass
    return False

def write_kudo_to_csv(work_id, writer, errorwriter):
    '''
    work_id is the AO3 ID of a work
    writer is a csv writer object
    the output of this program is a row in the CSV file containing works ID and
        username who gave it kudos
    header_info should be the header info to encourage ethical scraping.
    '''
    print('Scraping ', work_id)

    url = 'http://archiveofourown.org/works/'+str(work_id)+'/kudos'

    req = requests.get(url, headers=HTTP_HEAD)
    if req.status_code != 200:
        print('Access Denied')
        error_row = [work_id] + ['Access Denied']
        errorwriter.writerow(error_row)
        return

    src = req.text
    soup = BeautifulSoup(src, 'html.parser')

    if access_denied(soup):
        print('Access Denied')
        error_row = [work_id] + ['Access Denied']
        errorwriter.writerow(error_row)
    else:
        try:
            kudo_soup = soup.find(id="kudos").find_all('a')
            # Convert to set then back to list to remove duplicates
            kudo_list = [x.text for x in list(set(kudo_soup))]
        except AttributeError:
            kudo_list = []
        for kudo in kudo_list:
            row = [work_id] + [kudo]
            try:
                writer.writerow(row)
            except csv.Error:
                print('Unexpected error: ', sys.exc_info()[0])
                error_row = [work_id] +  [sys.exc_info()[0]]
                errorwriter.writerow(error_row)
        print('Done.')

def scrape(fandom, csv_in, csv_out, restart):
    """ Scrape the kudos from a list of fanwork_ids """

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
                header = ['work_id', 'user']
                writer.writerow(header)
            with open(csv_in, 'r+') as f_in:
                reader = csv.reader(f_in)
                if restart is '':
                    for i, row in enumerate(reader):
                        if i == 0:      # Skip header row
                            continue
                        write_kudo_to_csv(row[0], writer, errorwriter)
                        time.sleep(DELAY)
                else:
                    found_restart = False
                    for row in reader:
                        if not row:
                            continue
                        found_restart = process_id(row[0], restart, found_restart)
                        if found_restart:
                            write_kudo_to_csv(row[0], writer, errorwriter)
                            time.sleep(DELAY)
                        else:
                            print('Skipping already processed work')

def main():
    """ Open file and do the scraping """
    fandom, csv_in, csv_out, restart = get_args()
    scrape(fandom, csv_in, csv_out, restart)

if __name__ == "__main__":
    main()
