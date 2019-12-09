
from gather.ao3structures import Search
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse
import math 
import time
import sys

class ListScraper(object):
    
    def __init__(self, config):
        ''' Docstrings TODO '''
        
        self.params = config['params']
        self.output_file = config['files']['output']
        self.wait_time = config['delay']
        self.base_url = ''
        self.searchURL = Search(config['type_of'], self.params)

    def scrape(self):
        ''' Docstring TODO '''

        # Grab First Page
        self.base_url = self.searchURL.generateURL(page=1)
        print("Searching for work id's starting on page 1 here: ", self.base_url)
        with urllib.request.urlopen(self.base_url) as f:
            soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
        
        # Write header line of output
        with open(self.output_file, "w") as out:
            out.write(self.base_url+"\n")

        # Grab info for each page
        work_blurb_groups = soup.find_all(class_="work blurb group")
        for work in work_blurb_groups:
            with open(self.output_file, "a") as out:
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
        pages = self._gen_urls(max_pages)

        for i, page in enumerate(pages):
            time.sleep(self.wait_time)
            bar.update(i+1)

            with urllib.request.urlopen(page) as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
            work_blurb_groups = soup.find_all(class_="work blurb group")
            for work in work_blurb_groups:
                with open(self.output_file, "a") as out:
                    x = work.find('a').get('href').lstrip('/works/')
                    out.write(x+"\n")

        return

    
    def _gen_urls(self, max_pages):
        ''' Generate each subpage '''
        for i in range(2, max_pages+1):
            yield self.searchURL.generateURL(page=i)
        return
