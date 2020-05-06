''' In progress refactoring of meta scraping functionality.'''
import time
import datetime
from typing import Generator, List, Tuple, Any

from urllib.parse import quote
from bs4 import BeautifulSoup
from unidecode import unidecode

from scrape.page import Page
import utils.paths as paths
import config as cfg


class Meta(Page):

    def __init__(self, fandom: str, from_top: bool = True):
        self.log_path = paths.meta_log_path(fandom)
        self.meta_path = paths.meta_path(fandom)
        url = (f'https://archiveofourown.org/tags/'
               f'{quote(fandom, safe="")}/works?page=')
        super().__init__(fandom, 'meta',
                         self.log_path,
                         self.meta_path,
                         url,
                         from_top)

    def scrape(self):
        header = ['work_id', 'title', 'author', 'gifted', 'rating',
                  'warnings', 'category', 'status', 'fandom',
                  'relationship', 'character', 'additional tags',
                  'summary', 'language', 'words', 'chapters',
                  'collections', 'comments', 'kudos', 'bookmarks',
                  'hits', 'series_part', 'series_name', 'updated',
                  'scrape_date']
        super().scrape(header)

    def _pages(self) -> Generator[Tuple[BeautifulSoup, str], None, None]:

        try:
            page_num = int(self.last)
        except ValueError:
            self.logger.error(f'Last scraped value ({self.last})'
                              f' in .meta is not a number')
            raise ValueError

        if page_num == -1 or self.from_top is True:
            page_num = 1
        else:
            page_num += 1
        errors = 0

        self.logger.info(f"Scraping: {self.base_url}")
        try:
            max_pages = self._total_pages()
        except ConnectionError:
            self.logger.error(f'Base URL: {self.base_url} Not found.')
            raise ConnectionError(f"Error connecting to: {self.base_url}\n"
                                  f"Could your fandom name be incorrect?")
        except Exception as e:
            self.logger.error(f'Base URL: {self.base_url} Not found.')
            raise Exception(f"Other error: {e}")

        while errors < cfg.MAX_ERRORS and page_num <= max_pages:
            try:
                url = self.base_url + str(page_num)
                soup = self._get_soup(url)
            except ConnectionError:
                # 404 errors just move onto next page
                self.logger.error(f'PAGE: {url} 404 Error. Skipping this work.'
                                  f' {cfg.MAX_ERRORS-errors} attempts left.')
                errors += 1
                time.sleep(cfg.DELAY)
                page_num += 1
                url = self.base_url + str(page_num)
            except Exception:
                # all other time out errors don't move onto next page yet
                errors += 1
                self.logger.error(f'PAGE: {url} Not found. '
                                  f'{cfg.MAX_ERRORS-errors} attempts left.')
                time.sleep(cfg.DELAY*errors)   # exponential decay wait
            else:
                self.logger.info(f'Scraping PAGE: {str(page_num)}')
                time.sleep(cfg.DELAY)
                yield (soup, str(page_num))
                page_num += 1
                url = self.base_url + str(page_num)

    def _page_elements(self, page: BeautifulSoup) -> Generator[List[str],
                                                               None, None]:
        """ Find each HTML element and parse out the details into a row. """

        scrape_date = datetime.datetime.now().strftime("%d/%b/%Y %H:%M")

        works = page.find_all(class_="work blurb group")
        for work in works:
            tags = self._get_tags(work)
            req_tags = self._get_required_tags(work)
            stats = self._get_stats(work)
            header_tags = self._get_header(work)
            fandoms = self._get_fandoms(work)
            summary = self._get_summary(work)
            updated = self._get_updated(work)
            series = self._get_series(work)
            row = header_tags + req_tags + fandoms + \
                list(map(lambda x: ', '.join(x), tags)) + summary + stats + \
                series + updated + [scrape_date]
            yield row

    def _total_pages(self) -> int:
        ''' Make max attempts at loading base url to get starting number'''

        for attempts in range(cfg.MAX_ERRORS):
            try:
                soup = self._get_soup(self.base_url)
                next_element = soup.find('li', class_='next')
                max_pages = int(next_element.find_previous('li').text)
                self.logger.info(f'Attempting to scrape up to '
                                 f'{str(max_pages)} pages.')
                return max_pages
            except AttributeError:
                self.logger.info(f'Attempting to scrape 1 page.')
                return 1
            except ConnectionError:
                self.logger.error(f'Base URL: {self.base_url} Not found. '
                                  f'{cfg.MAX_ERRORS-attempts} attempts left.')
        raise Exception
        return 0

    def _get_tags(self, meta: BeautifulSoup) -> Any:
        """Find relationships, characters, and freeforms tags"""

        tags = ['relationships', 'characters', 'freeforms']
        return list(map(lambda tag: self._get_tag_info(tag, meta), tags))

    def _get_tag_info(self, category: str, meta: BeautifulSoup) -> List[str]:
        """ Find relationships, characters, and freeforms tags."""
        try:
            tag_list = meta.find_all("li", class_=category)
        except AttributeError:
            return []
        return [unidecode(result.text) for result in tag_list]

    def _get_required_tags(self, work: BeautifulSoup) -> List[str]:
        """Finds required tags."""

        req_tags = work.find(class_='required-tags').find_all('a')
        return [x.text for x in req_tags]

    def _get_stats(self, work: BeautifulSoup) -> List[str]:
        """
        Find stats (language, published, status, date status, words, chapters,
        comments, kudos, bookmarks, hits
        """

        categories = ['language', 'words', 'chapters', 'collections',
                      'comments', 'kudos', 'bookmarks', 'hits']
        stats = []
        for cat in categories:
            try:
                result = work.find("dd", class_=cat).text
            except AttributeError:
                result = ""
            stats.append(result)
        return stats

    def _get_header(self, work: BeautifulSoup) -> List[str]:
        '''Finds header information
           (work_id, title, author, gifted to user).'''

        result = work.find('h4', class_='heading').find_all('a')
        work_id = result[0].get('href').strip('/works/')
        title = result[0].text

        auth_list = []
        header_text = work.find('h4', class_='heading').text
        if "Anonymous" in header_text:
            auth = "Anonymous"
        else:
            authors = work.find_all('a', rel='author')
            for author in authors:
                auth_list.append(author.text)
            auth_str = str(auth_list)
            auth = auth_str.replace('[', '').replace(']', '').replace("'", '')

        gift_list = []
        for link in result:
            href = link.get('href')
            if 'gifts' in href:
                gift_list.append(link.text)

        if len(gift_list) == 0:
            gift = ""
        else:
            gift_str = str(gift_list)
            gift = gift_str.replace('[', '').replace(']', '').replace("'", '')

        return [work_id, title, auth, gift]

    def _get_fandoms(self, work: BeautifulSoup) -> List[str]:
        """ Find the list of fandoms."""

        fandoms = ''
        try:
            tag_list = work.find('h5', class_='fandoms heading').find_all('a')
            fan_list = [x.text for x in tag_list]
            fandoms = ", ".join(fan_list)
        except AttributeError:
            return []
        return [fandoms]

    def _get_summary(self, work: BeautifulSoup) -> List[str]:
        """ Find summary description and return as list of strings. """

        try:
            summary_string = work.find('blockquote',
                                       class_='userstuff summary')
            summary = summary_string.text.strip().replace('\n', ' ')
        except AttributeError:
            summary = ""
        return [summary]

    def _get_updated(self, work: BeautifulSoup) -> List[str]:
        """ Find update date. Return as list of strings. """

        try:
            date = work.find('p', class_='datetime').text
        except AttributeError:
            date = ""
        return [date]

    def _get_series(self, work: BeautifulSoup) -> List[str]:
        """ Find series info and return as list. """

        try:
            series = work.find('ul', class_='series')
            part = series.find('strong').text
            s_name = series.find('a').text
        except AttributeError:
            part, s_name = "", ""
        return [part, s_name]
