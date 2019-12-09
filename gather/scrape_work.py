# script to scrape data from AO3
from gather.ao3structures import Work
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse
import math 
import time
import sys
import json

class PageScraper():
    def __init__(self, id):
        self.url = "https://archiveofourown.org/works/" + str(id) + "?view_adult=true&amp;view_full_work=true"
        self.fanWork = Work(id, self.url)
        
    def scrape(self):
        ''' Scrapes the contents of the page '''
        
        try:
            with urllib.request.urlopen(self.url) as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
        except:
            print("Error reading page")
            return

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
        self.fanWork.comments_count = self._get_comments_count(soup) # TODO ERROR
        self.fanWork.kudos_count = self._get_kudos_count(soup)  
        self.fanWork.bookmarks_count = self._get_bookmarks_count(soup)
        self.fanWork.hits = self._get_hits_count(soup)
        self.fanWork.author = self._get_author(soup)

    
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

    def _get_author(self, soup):
        pass
        return False


    def print(self):
        self.fanWork.print()


