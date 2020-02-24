import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import requests
import os
import csv
import sys
import datetime
import argparse

def get_args():

    parser = argparse.ArgumentParser(description='Scrape AO3 work IDs to find all named users who gave kudos')
    parser.add_argument('--in_csv', default='fanworks_ids.csv',help='csv input file name')
    parser.add_argument('--out_csv', default='fanworks_kudos.csv',help='csv output file name')
    parser.add_argument('--restart', default='', help='work_id to start at from within a csv')
    parser.add_argument('--header', default='', help='user http header')

    args = parser.parse_args()
    output_file = str(args.out_csv)
    input_file = str(args.in_csv)
    restart = str(args.restart)
    headers = str(args.header)

    return input_file, output_file, restart, headers

def process_id(work_id, restart, found):
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
    if (soup.find(class_="flash error")):
        pass
    return False

def write_kudo_to_csv(work_id, writer, errorwriter, header_info=''):
    '''
    work_id is the AO3 ID of a work
    writer is a csv writer object
    the output of this program is a row in the CSV file containing works ID and 
        username who gave it kudos
    header_info should be the header info to encourage ethical scraping.
    '''
    print('Scraping ', work_id)

    url = 'http://archiveofourown.org/works/'+str(work_id)+'/kudos'
    headers = {'user-agent' : header_info}
    
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        print('Access Denied')
        error_row = [work_id] + ['Access Denied']
        errorwriter.writerow(error_row)
        return

    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    
    if (access_denied(soup)):
        print('Access Denied')
        error_row = [work_id] + ['Access Denied']
        errorwriter.writerow(error_row)
    else:
        try:
            kudo_soup = soup.find(id="kudos").find_all('a')
            # Convert to set then back to list to remove duplicates
            kudo_list = [x.text for x in list(set(kudo_soup))]  
        except AttributeError as e:
            kudo_list = []
        for kudo in kudo_list:
            row = [work_id] + [kudo]
            try:
                writer.writerow(row)
            except:
                print('Unexpected error: ', sys.exc_info()[0])
                error_row = [work_id] +  [sys.exc_info()[0]]
                errorwriter.writerow(error_row)
        print('Done.')

def main():

    csv_in, csv_out, restart, headers = get_args()
    delay = 5
    os.chdir(os.getcwd())
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
                    for row in reader:
                        if not row:
                            continue
                        write_kudo_to_csv(row[0], writer, errorwriter, headers)
                        time.sleep(delay)
                else: 
                    found_restart = False
                    for row in reader:
                        if not row:
                            continue
                        found_restart = process_id(row[0], restart, found_restart)
                        if found_restart:
                            write_kudo_to_csv(row[0], writer, errorwriter, headers)
                            time.sleep(delay)
                        else:
                            print('Skipping already processed work')

if __name__ == "__main__":
    main()