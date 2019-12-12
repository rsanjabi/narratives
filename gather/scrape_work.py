# script to scrape data from AO3
from gather.ao3structures import Work, Comment
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse
import math 
import time
import sys
import json

class WorkScraper():
    def __init__(self, id):
        self.url = "https://archiveofourown.org/works/" + str(id) + "?view_adult=true&amp;view_full_work=true"
        self.fanWork = Work(id, self.url)

    def print(self):
        self.fanWork.print()
        
    def scrape(self):
        ''' Scrapes the contents of the page '''
        print("Debug start scraping")
        try:
            with urllib.request.urlopen(self.url) as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
        except:
            print("Error reading works page. ", self.url)
            return
        print("Debug start parsing")
        self.fanWork.rating = self._get_rating(soup)
        self.fanWork.archive_warnings = self._get_warning(soup)
        self.fanWork.categories = self._get_categories(soup)
        self.fanWork.fandoms = self._get_fandoms(soup)
        self.fanWork.relationships = self._get_relationships(soup)
        self.fanWork.characters = self._get_characters(soup)
        self.fanWork.additional_tags = self._get_additional_tags(soup)
        self.fanWork.language = self._get_language(soup)
        self.fanWork.published = self._get_published(soup)
        self.fanWork.updated = self._get_updated(soup)
        self.fanWork.words = self._get_words(soup)
        self.fanWork.chapter_current_count, self.fanWork.chapter_max_count = self._get_chapter_count(soup)
        self.fanWork.comments_count = self._get_comments_count(soup) # TODO ERROR (OR MAYBE NOT?)
        self.fanWork.kudos_count = self._get_kudos_count(soup)  
        self.fanWork.bookmarks_count = self._get_bookmarks_count(soup)
        self.fanWork.hits = self._get_hits_count(soup)
        self.fanWork.author_pseud, self.fanWork.author_user = self._get_author(soup)
        self.fanWork.title = self._get_title(soup)
        self.fanWork.gift = self._get_gift(soup)
        self.fanWork.series = self._get_series(soup)
        self.fanWork.collection_ref, self.fanWork.collection_name = self._get_collections(soup) # fix so that it grabs multiple pairs
        self.fanWork.associations = self._get_associations(soup)

        print("Debug start kudo crawl")
        # Crawl to kudos page
        self.fanWork.kudo_guest_count, self.fanWork.kudos = self._crawl_kudos(soup)
        
        print("Debug start comment scraping")
        # Crawl comments
        self.fanWork.comments = self._crawl_comments(soup)

        # Crawl bookmarks
        "https://archiveofourown.org/works/14388135/bookmarks"
        pass

    def _crawl_comments(self, soup):
        # Crawl throught all the pages returning a list of comments
        comment_list = []
        pages_soup = self._crawl_comment_pages()
        for page in pages_soup:
            comments_blurb = self._get_comments_blurbs(page) 
            for comment in comments_blurb:
                comment_list.append(self._get_a_comment(comment)) 
        return comment_list
        
    def _crawl_comment_pages(self):
        # Crawl a each page of comments returning that pages soup
        print("Debug grab first comment page")
        try:
            comments_url = 'https://archiveofourown.org/comments/show_comments?page=1&view_full_work=true&work_id=' + str(self.fanWork.id)
            with urllib.request.urlopen(comments_url) as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
                pagination_blurb = soup.find(class_='pagination actions')
                page_counts = [page.get_text() for page in pagination_blurb.find_all('li')]
                max_pages = int(page_counts[-2:-1][0])
        except:
            print("Error reading comments.", comments_url)

        for i in range(1, max_pages+1):
            try:
                print("DEBUG Page#", i)
                comments_url = 'https://archiveofourown.org/comments/show_comments?page='+ str(i) + '&view_full_work=true&work_id=' + str(self.fanWork.id)
                with urllib.request.urlopen(comments_url) as f:
                    soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
                yield soup
            except:
                print("Error reading comment page #", str(i), comments_url)
        return

    def _get_comments_blurbs(self, soup):
        # Generator returning sub-soup/blurb of a comment
        comment_blurb = soup.find(class_='thread').find_all(role='article')
        for comment in comment_blurb:
            yield comment
        return

    def _get_a_comment(self, comment_soup):
        # Extracts the details of comment
    

        try:
            byline = comment.find(class_='heading byline').get_text()
            user = byline.split('on')[0].strip()
            byline = byline.split()
            date_time = " ".join(byline[-7:-1])
            chapter_num = byline[3]
            comment_text = 0
            reply_to = 0
            id = 0
            edit_date = 0
            return Comment(user, chapter_num, date_time, comment_text, reply_to, id, edit_date)
        except:
            return None

    def _get_rating(self, soup):
        # Get one rating back
        try:
            return soup.find_all(class_="rating tags")[1].get_text().strip()
        except:
            print("Error grabbing rating.")

    def _get_warning(self, soup):
        # Get a list of warnings
        try:
            warnings = soup.find_all(class_="warning tags")[1].find_all('li')
            warning_list = [warning.get_text().strip() for warning in warnings]
            return warning_list
        except:
            print("Error grabbing archive warnings.")
            return

    def _get_categories(self, soup):
        # Get a list of (relationship) categories
        try:
            categories = soup.find_all(class_="category tags")[1].find_all('li')
            category_list = [category.get_text().strip() for category in categories]
            return category_list
        except:
            print("Error grabbing categories.")
            return

    def _get_fandoms(self, soup):
        # Get a list of fandoms
        try:
            fandoms = soup.find_all(class_="fandom tags")[1].find_all('li')
            fandom_list = [fandom.get_text().strip() for fandom in fandoms]
            return fandom_list
        except:
            print("Error grabbing fandoms.")
            return

    def _get_relationships(self, soup):
        # Get a list of relationships
        try:
            ships = soup.find_all(class_="relationship tags")[1].find_all('li')
            ship_list = [ship.get_text().strip() for ship in ships]
            return ship_list
        except:
            print("Error grabbing relationships.")
            return

    def _get_characters(self, soup):
        # Get a list of characters
        try:
            characters = soup.find_all(class_="character tags")[1].find_all('li')
            char_list = [char.get_text().strip() for char in characters]
            return char_list
        except:
            print("Error grabbing characters.")
            return

    def _get_additional_tags(self, soup):
        # Get a list of additional tags
        try:
            add_tags = soup.find_all(class_="freeform tags")[1].find_all('li')
            add_tag_list = [tag.get_text().strip() for tag in add_tags]
            return add_tag_list
        except:
            print("Error grabbing additional tags.")
            return

    def _get_language(self, soup):
        # Get language
        try:
            return soup.find_all(class_="language")[1].get_text().strip()
        except:
            print("Error grabbing language.")

    def _get_published(self, soup):
        # Get published date 
        try:
            return soup.find_all(class_="published")[1].get_text().strip()
        except:
            print("Error grabbing published date.")

    def _get_updated(self, soup): # optional
        # Get updated date 
        try:
            return soup.find_all(class_="status")[1].get_text().strip()
        except:
            print("Error grabbing updated date.")

    def _get_words(self, soup):
        # Get word count  
        try:
            return soup.find_all(class_="words")[1].get_text().strip()
        except:
            print("Error grabbing word count.")

    def _get_chapter_count(self, soup):
        # Get chapters
        # TODO how to deal with single chapters 
        try:
            chapters = soup.find_all(class_="chapters")[1].get_text().strip()
            current,total = chapters.split('/')
            return current, total
        except:
            print("Error grabbing published date.")

    def _get_comments_count(self, soup):
        # Get total comments 
        try:
            return soup.find_all(class_="comments")[2].get_text().strip()
        except:
            print("Error grabbing total comment count.")

    def _get_kudos_count(self, soup):
        # Get total kudos count 
        try:
            return soup.find_all(class_="kudos")[1].get_text().strip()
        except:
            print("Error grabbing total kudos count.")

    def _get_bookmarks_count(self, soup):
        # Get total bookmarks 
        try:
            return soup.find_all(class_="bookmarks")[1].get_text().strip()
        except:
            print("Error grabbing total bookmark count.")

    def _get_hits_count(self, soup):
        # Get total hits 
        try:
            return soup.find_all(class_="hits")[1].get_text().strip()
        except:
            print("Error grabbing total hits count.")

    def _get_title(self, soup):
        # Get title 
        try:
            return soup.find(class_="title heading").get_text().strip()
        except:
            print("Error grabbing title.")

    def _get_author(self, soup):
        # Get author 
        psued = ''
        primary = ''
        try:
            user_entire = soup.find(class_="byline heading").get_text().strip()
            if ' ' in user_entire:
                psued, primary = user_entire.split()
                primary = primary.lstrip('(').rstrip(')')
            else:
                primary = user_entire
                psued = user_entire
            return psued, primary
        except:
            print("Error grabbing author.")

    def _get_gift(self, soup):
        # Get gift recipient 
        try:
            association_blurb = soup.find(class_="associations")
            recipient = association_blurb.find_all('li')[0].find('a').get_text()
            return  recipient
        except:
            print("Error grabbing gift recipient.")

    def _get_series(self, soup):
        # Get series info 
        series_dict = {}

        try:
            series_blurb = soup.find(class_='position')
            part, name = series_blurb.get_text().lstrip('Part ').split(' of the ')
            name = name.rstrip(' series')
            series_dict['position'] = part
            series_dict['series_name'] = name
            series_dict['series_id'] = series_blurb.find('a').get('href').strip('/series/')
            return series_dict
        except:
            print("Error grabbing series info.")

    def _get_collections(self, soup):
        # Get collection info 

        # TODO get all collections return as list
        try:
            collection_blurb = soup.find_all(class_="collections")[1]
            collection_ref = collection_blurb.find('a').get('href').lstrip('/collections/')
            collection_name = collection_blurb.get_text().strip()
            return collection_ref, collection_name
        except:
            print("Error grabbing title.")

    def _get_associations(self, soup):
        # Get translations/associations 
        # TODO reciprical scraping

        try:
            associations_blurb = soup.find(class_='associations').find_all('li')[1]
            associated_id = associations_blurb.find('a').get('href').lstrip('/works/')
            return associated_id
        except:
            print("Error grabbing translated/associated works.")

    def _crawl_kudos(self, soup):
        # Get list of users who gave kudos and number of guests who kudo'd
        
        kudos_url = "https://archiveofourown.org/works/" + str(self.fanWork.id) + "/kudos"
        try:

            with urllib.request.urlopen(kudos_url) as f:
                kudo_soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
                guest_count, users = self._get_kudos(kudo_soup)
                return guest_count, users
        except:
            print("Error reading kudos page.", kudos_url)

    def _get_kudos(self, soup):
        # get a list of users who kudo'd
        try:
            user_list_soup = soup.find(class_="kudos")
            _, guest_text = user_list_soup.get_text().split('as well as')
            guest_count = guest_text.replace('\n', '').strip().rstrip('guests left kudos on this work!')
            kudo_names = [user.get_text() for user in user_list_soup.find_all('a')]
            return guest_count, kudo_names
        except:
            print("Error grabbing title.")
            return '', ''

   