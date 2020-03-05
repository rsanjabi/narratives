import requests
from bs4 import BeautifulSoup
import argparse
import time
import os
import csv
import sys
from unidecode import unidecode

DATA_PATH = '../../data/raw/meta/'

def get_tag_info(category, meta):
    '''
    given a category and a 'work meta group, returns a list of tags (eg, 'rating' -> 'explicit')
    '''
    try:
        tag_list = meta.find("dd", class_=str(category) + ' tags').find_all(class_="tag")
    except AttributeError as e:
        return []
    return [unidecode(result.text) for result in tag_list] 

def get_stats(meta):
    '''
    returns a list of  
    language, published, status, date status, words, chapters, comments, kudos, bookmarks, hits
    '''
    categories = ['language', 'published', 'status', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits'] 

    stats = list(map(lambda category: meta.find("dd", class_=category), categories))

    if not stats[2]:
        stats[2] = stats[1] #no explicit completed field -- one shot
    try:    
        stats = [unidecode(stat.text) for stat in stats]
    except AttributeError as e: #for some reason, AO3 sometimes miss stat tags (like hits)
        new_stats = []
        for stat in stats:
            if stat: new_stats.append(unidecode(stat.text))
            else: new_stats.append('null')
        stats = new_stats

    stats[0] = stats[0].rstrip().lstrip() #language has weird whitespace characters
    #add a custom completed/updated field
    status  = meta.find("dt", class_="status")
    if not status: status = 'Completed' 
    else: status = status.text.strip(':')
    stats.insert(2, status)

    return stats      

def get_tags(meta):
    '''
    returns a list of lists, of
    rating, category, fandom, pairing, characters, additional_tags
    '''
    tags = ['rating', 'category', 'fandom', 'relationship', 'character', 'freeform']
    return list(map(lambda tag: get_tag_info(tag, meta), tags))

def access_denied(soup):
    if (soup.find(class_="flash error")):
        return True
    if (not soup.find(class_="work meta group")):
        return True
    return False

def write_fic_to_csv(fandom, writer, errorwriter, header_info=''):
    '''
    fic_id is the AO3 ID of a fic, found every URL /works/[id].
    writer is a csv writer object
    the output of this program is a row in the CSV file containing all metadata 
    and the fic content itself.
    header_info should be the header info to encourage ethical scraping.
    '''
    print('Scraping ', fandom)
    url = 'https://archiveofourown.org/tags/'+str(fandom)+'/works'
    headers = {'user-agent' : header_info}
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'html.parser')
    if (access_denied(soup)):
        print('Access Denied')
        error_row = [fandom] + ['Access Denied']
        errorwriter.writerow(error_row)
    '''
    else:
        meta = soup.find("dl", class_="work meta group")
        tags = get_tags(meta)
        stats = get_stats(meta)
        title = unidecode(soup.find("h2", class_="title heading").string).strip()
        #get the fic itself
        content = soup.find("div", id= "chapters")
        chapters = content.select('p')
        chaptertext = '\n\n'.join([unidecode(chapter.text) for chapter in chapters])
        row = [fic_id] + [title] + list(map(lambda x: ', '.join(x), tags)) + stats + [chaptertext]
        #fandom?
        try:
            writer.writerow(row)
        except:
            print('Unexpected error: ', sys.exc_info()[0])
            error_row = [fic_id] +  [sys.exc_info()[0]]
            errorwriter.writerow(error_row)
        print('Done.')
    '''

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
    fandoms = args.fandom
    is_csv = (len(fandoms) == 1 and '.csv' in fandoms[0]) 
    csv_out = str(args.csv)
    headers = str(args.header)
    restart = str(args.restart)
    return fandoms, csv_out, headers, restart, is_csv

def process_id(fic_id, restart, found):
    if found:
        return True
    if fic_id == restart:
        return True
    else:
        return False

def scrape(fandoms, csv_out, headers, restart, is_csv):
    delay = 5
    os.chdir(os.getcwd())
    with open(DATA_PATH+csv_out, 'a') as f_out:
        writer = csv.writer(f_out)
        with open(DATA_PATH+"errors_" + csv_out, 'a') as e_out:
            errorwriter = csv.writer(e_out)
            #does the csv already exist? if not, let's write a header row.
            if os.stat('../../data/'+csv_out).st_size == 0:
                print('Writing a header row for the csv.')
                header = ['work_id', 'title', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body']
                #header = ['work_id', 'title', 'author', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'body', 'archive_warnings', 'summary', 'series_part', 'series_name', 'collections', 'scrape_date']
                writer.writerow(header)
            if is_csv:
                csv_fname = fandoms[0]
                with open(DATA_PATH + "errors_" + csv_fname, 'r+') as f_in:
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
                for fandom in fandoms:
                    write_fic_to_csv(fandom, writer, errorwriter, headers)
                    time.sleep(delay)

if __name__== "__main__":
    fandoms, csv_out, headers, restart, is_csv = get_args()
    scrape(fandoms, csv_out, headers, restart, is_csv)