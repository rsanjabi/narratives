# Class defining work data structure
import urllib
from datetime import datetime
import json
import pytz

class Work:
    def __init__(self, id, url):
        ''' Constructor for this class. '''
        self.id = id                    # Number in string format from '2' to approximately '21841285'
        self.url = url                  # Url of work; view_adult = true; view_full_work = true
        self.scrape_date = str(datetime.now(tz=pytz.utc))   # today's date and time in utc
        self.rating = ''                # 1 of 5 possible ratings
        self.archive_warnings = []      # 0 to 6 warnings
        self.categories = []            # 0 to 6 relationship categories
        self.fandoms = []               # 1 to M
        self.relationships = []         # 0 to M
        self.characters = []            # 0 to M
        self.additional_tags = []       # 0 to M
        self.language = ''              # 1 language
        self.published = ''             # 1 published date string format
        self.updated = ''               # 0 to 1 updated date
        self.words = ''                 # Number of words in string format '0' to really big
        self.chapter_current_count = '' # 1 to Big number
        self.chapter_max_count = ''     # ? or 1 to big number
        self.hits = ''                  # n/a, 0 or 1 to big number
        self.kudos_total_count = ''     # n/a, 0 to big number
        self.kudo_guest_count = ''      # n/a, 1 to big number
        self.kudos_users = []           # list of users
        self.creator_pseud = ''         # user/pseud - can't have some characters
        self.creator_user = ''          # user/primary - can't have some characters
        self.title = ''                 # String including special characters from 1(?) to M long
        self.bookmarks_count = ''       # 1 to M (10018 is largest)
        self.gift = ''                  # n/a, 1 to M user(s) work was gifted for. May or may not be users
        self.series = {}                # n/a, series id, name, position
        self.collection_name = ''       # n/a, 1 to many collections
        self.collection_ref = ''        
        self.associations = []          # a list of associations (translations or original_source)
        self.meta_notes = {}            # a  dict {'all': Chapter, '1': Chapter, 'end': Chapter}
        self.body_non_text = ''         # detects things like links or images

        self.comments_count = ''        # n/a, 1 to M
        self.comments = []              # a list of comment objects
        self.bookmarks = []             # a list of bookmark objects


    def print(self):
        print(json.dumps(vars(self), sort_keys=True, indent=4))

class Chapter:
    def __init__(self, title, summary, notes, body):
        self.title = title
        self.summary = summary
        self.notes = notes
        self.body = body

class Comment:
    def __init__(self, user, chapter_num, date_time, comment_text, reply_to, id, edit_date):
        self.user = user 
        self.chapter_num = chapter_num
        self.date_time = date_time
        self.comment_text = comment_text
        self.reply_to = reply_to
        self.id = id
        self.edit_date = edit_date

class Bookmark:
    def __init__(self, user, date, tags, comments):
        self.user = user 
        self.tags = tags
        self.date = date
        self.comments = comments

class Search:
    def __init__(self, type_of, config):
        self.type_of = type_of
        self.params = config

    def generateURL(self, page=1):
        # generate urls

        self.params['page'] = page
        params = urllib.parse.urlencode(self.params)
        url = "https://archiveofourown.org/" + self.type_of + "?%s" % params

        return url

class Translation:
    ''' object for either source object or in case of translation works points to original'''

    def __init__(self, translator, translated_id, language):
        self.language = language
        self.translator = translator
        self.translated_id = translated_id
