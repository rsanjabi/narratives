
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse
import math 
import time
import sys

def initial_url(tag, type_of="works", sort='date_posted', date_from='all'):
    # generate url
    ''' 
    type_of = 'works' or 'bookmarks'
    tag = string, tested on fandom name tags, but possibly any tags?
    sort = 'date_posted' any other sort may not work???
    date_from = defaults to all otherwise assume '2017-12-01' format December 1, 2017
    '''

    url_params = {'utf8': '✓', 
                    'commit': 'Sort and Filter', 
                    'work_search[sort_column]':'',
                    'work_search[other_tag_names]': '', 
                    'work_search[excluded_tag_names]': '',
                    'work_search[crossover]': '',
                    'work_search[complete]': '',
                    'work_search[words_from]': '',
                    'work_search[words_to]': '',
                    'work_search[date_from]': '',
                    'work_search[date_to]': '',
                    'work_search[query]': '',
                    'work_search[language_id]': '',
                    'tag_id': tag,
                    'page': ''
                    }
    if sort == 'date_posted':
        url_params['work_search[sort_column]'] = 'created_at'
    if date_from != 'all':
        url_params['work_search[date_from]'] = date_from

    params = urllib.parse.urlencode(url_params)
    
    url = "https://archiveofourown.org/" + type_of + "?%s" % params

    return url, url_params

def gen_urls(url_params, type_of, max_pages):
    ''' Generate each subpage '''

    for i in range(2, max_pages+1):
        url_params['page'] = i
        params = urllib.parse.urlencode(url_params)
        url = "https://archiveofourown.org/" + type_of + "?%s" % params
        yield url
    return

def get_works_list(output_file, tag, type_of, sort, date_from):

    base_url, url_params = initial_url(tag, type_of, sort, date_from)
    print("Searching for work id's starting on page 1 here: ", base_url)

    with urllib.request.urlopen(base_url) as f:
        soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
    work_blurb_groups = soup.find_all(class_="work blurb group")
    with open(output_file, "w") as out:
            out.write(base_url+"\n")
    for work in work_blurb_groups:
        with open(output_file, "a") as out:
            a = work.find('a').get('href').lstrip('/works/')
            out.write(a+"\n")
    
    # Find max number of pages
    try:
        heading = soup.find('h2')
        count = heading.get_text().split(' Works in ')[0].strip()
        if (count.isnumeric()):
            max_pages = 1
        else:
            num_works = int(count.split(' of ')[1])
            max_pages = math.ceil(num_works/20)
    except:
        print("Error trying to compute number of pages to scrape.")
        sys.exit()

    bar = progressbar.ProgressBar(max_value=max_pages)
    bar.update(1)
    pages = gen_urls(url_params, type_of, max_pages)

    for i, page in enumerate(pages):
        time.sleep(1)
        bar.update(i+1)

        with urllib.request.urlopen(page) as f:
            soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
        work_blurb_groups = soup.find_all(class_="work blurb group")
        for work in work_blurb_groups:
            with open(output_file, "a") as out:
                x = work.find('a').get('href').lstrip('/works/')
                out.write(x+"\n")

    return


