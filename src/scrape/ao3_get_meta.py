import requests
from bs4 import BeautifulSoup
import argparse
import time
import os
import csv
import sys
from unidecode import unidecode
from pathvalidate import replace_symbol, is_valid_filename
from urllib.parse import quote


def get_tag_info(category, meta):
    '''
    given a category and a 'work meta group, returns a list of tags (eg, 'rating' -> 'explicit')
    '''
    try:
        tag_list = meta.find_all("li", class_=str(category))
    except AttributeError as e:
        return []
    return [unidecode(result.text) for result in tag_list] 

def get_stats(work):
    '''
    returns a list of  
    language, published, status, date status, words, chapters, comments, kudos, bookmarks, hits
    '''
    categories = ['language', 'words', 'chapters', 'collections', 'comments', 'kudos', 'bookmarks', 'hits'] 
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
    tags = ['warnings', 'relationships', 'characters', 'freeforms']
    return list(map(lambda tag: get_tag_info(tag, meta), tags))

def get_required_tags(work):
    req_tags = work.find(class_='required-tags').find_all('a')
    return [x.text for x in req_tags]

def write_fic_to_csv(fandom, writer, errorwriter, header_info=''):
    '''
    fic_id is the AO3 ID of a fic, found every URL /works/[id].
    writer is a csv writer object
    the output of this program is a row in the CSV file containing all metadata 
    and the fic content itself.
    header_info should be the header info to encourage ethical scraping.
    '''
    url = 'https://archiveofourown.org/tags/'+quote(fandom)+'/works'
    print('Scraping:', url)
    headers = {'user-agent' : header_info}
    #find out how many pages and then do for each page
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        print('Access Denied')
        error_row = [fandom] + ['Access Denied']
        errorwriter.writerow(error_row)
        return

    soup = BeautifulSoup(req.text, 'html.parser')
    works = soup.find_all(class_="work blurb group")
    for work in works:
        tags = get_tags(work)
        req_tags = get_required_tags(work)
        stats = get_stats(work)

        #title = unidecode(soup.find("h2", class_="title heading").string).strip()
        #row = [title] + list(map(lambda x: ', '.join(x), tags)) + req_tags #+ stats
        row = list(map(lambda x: ', '.join(x), tags)) + req_tags + stats
        try:
            writer.writerow(row)
        except:
            print('Unexpected error: ', sys.exc_info()[0])
            error_row = [fic_id] +  [sys.exc_info()[0]]
            errorwriter.writerow(error_row)

    print('Done.')


def get_args(): 
    parser = argparse.ArgumentParser(description='Scrape and save some fanfic, given their AO3 IDs.')
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
    is_csv = False               # Replace this with code to pick up a certain page number if interrupted
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
    delay = 2
    fandom_dir = replace_symbol(fandom)
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/raw/meta/'+fandom_dir)
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
                header = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body']
                #header = ['work_id', 'title', 'author', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body', 'archive_warnings', 'summary', 'series_part', 'series_name', 'collections', 'scrape_date']
                writer.writerow(header)
            if is_csv:
                with open("errors_" + csv_out, 'r+') as f_in:
                    reader = csv.reader(f_in)
                    if restart is '':
                        for row in reader:
                            if not row:
                                continue
                            write_fic_to_csv(row[0], writer, errorwriter, headers)
                            time.sleep(delay)
                    else: 
                        found_restart = False
                        for row in reader:
                            if not row:
                                continue
                            found_restart = process_id(row[0], restart, found_restart)  # TODO rewrite for restart to work restart at page??
                            if found_restart:
                                write_fic_to_csv(row[0], writer, errorwriter, headers)
                                time.sleep(delay)
                            else:
                                print('Skipping already processed fic')
            else:
                write_fic_to_csv(fandom, writer, errorwriter, headers)
                time.sleep(delay)


if __name__== "__main__":
    fandom, csv_out, headers, restart, is_csv = get_args()
    scrape(fandom, csv_out, headers, restart, is_csv)