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
    # add headers
    parser = argparse.ArgumentParser(description='Scrape AO3 work IDs to find all named users who gave kudos')
    parser.add_argument(
        '--in_csv', default='fanfics_metadata.csv',
        help='csv input file name')
    parser.add_argument(
        '--out_csv', default='fanfics_item_user.csv',
        help='csv output file name')
    parser.add_argument(
		'--restart', default='', 
		help='work_id to start at from within a csv')

    args = parser.parse_args()
    output_file = str(args.out_csv)
    input_file = str(args.in_csv)
    restart = str(args.restart)

    return input_file, output_file, restart

def main():

	csv_in, csv_out, restart = get_args()
	delay = 5
	os.chdir(os.getcwd())
	with open(csv_out, 'a') as f_out:
        writer = csv.writer(f_out)
        with open("kudo_errors_" + csv_out, 'a') as e_out:
            errorwriter = csv.writer(e_out)
            #does the csv already exist? if not, let's write a header row.
            if os.stat(csv_out).st_size == 0:
                print('Writing a header row for the csv.')
                header = ['user', 'work_id']
                writer.writerow(header)
            with open(csv_in, 'r+') as f_in:
                reader = csv.reader(f_in)
                if restart is '':
                    for row in reader:
                        if not row:
                            continue
                        #write_fic_to_csv(row[0], only_first_chap, writer, errorwriter, headers)
                        time.sleep(delay)
                else: 
                    found_restart = False
                    for row in reader:
                        if not row:
                            continue
                        #found_restart = process_id(row[0], restart, found_restart)
                        pass
                        if found_restart:
                            #write_fic_to_csv(row[0], only_first_chap, writer, errorwriter, headers)
                            time.sleep(delay)
                        else:
                            print('Skipping already processed fic')


if __name__ == "__main__":
    main()