
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse

def gen_url(tag, type_of="works", sort='date_posted'):
    # generate url
    #params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
    #url = "http://www.musi-cal.com/cgi-bin/query?%s" % params
    #print(url)

    # parse URL to handle more stuff
    # https://archiveofourown.org/works?utf8=%E2%9C%93&commit=Sort+and+Filter&work_search%5Bsort_column%5D=created_at&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=Star+Wars+-+All+Media+Types
    
    prefix = "https://archiveofourown.org/tags/"
    searchterm = urllib.parse.quote(tag) +"/"
    url = prefix + searchterm + type_of
    print(url)

    return url

def get_works_list(tag, type_of="works", sort='date_posted'):
    ''' type = "bookmarks" '''

    base_url = gen_url(tag, type_of, sort)
    with urllib.request.urlopen(base_url) as f:
        print(f.read().decode('utf-8'))
    # iterate through each page
    # scrape urls
    # write urls to text file
