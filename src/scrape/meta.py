''' In progress refactoring of meta scraping functionality.'''
import time
import datetime
from typing import Generator, List, Tuple, Any, Optional, Dict
from mypy_extensions import TypedDict
import json

from urllib.parse import quote
from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, HTTPError

from scrape.page import Page
import utils.paths as paths
from utils.progress import Progress
import config as cfg

MetaJson = TypedDict('MetaJson', {
                     'work_id': str,
                     'title': str,
                     'author': List[str],
                     'gifted': Optional[List[str]],
                     'rating': Optional[str],
                     'warnings': List[str],
                     'category': Optional[List[str]],
                     'status': str,
                     'fandom': List[str],
                     'relationships': Optional[List[str]],
                     'characters': Optional[List[str]],
                     'freeforms': Optional[List[str]],
                     'summary': Optional[str],
                     'language': str,
                     'words': int,
                     'chapters': int,
                     'collections': int,
                     'comments': int,
                     'kudos': int,
                     'bookmarks': int,
                     'hits': int,
                     'series_part': Optional[str],
                     'series_name': Optional[str],
                     'updated': Optional[str],
                     'scrape_date': str})


class Meta(Page):

    def __init__(self, tag: str, from_top: bool = True):
        self.base_url = (f'https://archiveofourown.org/tags/'
                         f'{quote(tag).replace(".", "*d*")}/works?page=')
        tag_path = paths.tag_path(tag)
        self.progress = Progress(tag_path)
        self.last = self.progress.read()[0]

        self.path = paths.meta_path(tag)
        log_path = paths.meta_log_path(tag)
        super().__init__(tag+'_meta', log_path)

        self.from_top = self._start_from_top(from_top)

    def scrape(self) -> None:

        if self.from_top is True or self.path.is_file() is False:
            mode = 'w'
        else:
            mode = 'a'

        with open(self.path, mode) as f_out:
            pages = self._pages()
            for page, progress_num in pages:
                page_elements = self._page_elements(page)
                for element in page_elements:
                    f_out.write(json.dumps(element)+'\n')
                self.progress.write(progress_num)
        self.logger.info(f'Completed scraping "{self.page_kind}"')
        return
        super().scrape()

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
            except HTTPError:
                # just move onto next page
                self.logger.error(f'PAGE: {url} 404 Error. Skipping this work.'
                                  f' {cfg.MAX_ERRORS-errors} attempts left.')
                errors += 1
                time.sleep(cfg.DELAY)
                page_num += 1
                url = self.base_url + str(page_num)
            except ConnectTimeout:
                # Try again
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

    def _page_elements(self, page: BeautifulSoup) -> Generator[MetaJson,
                                                               None, None]:
        """ Find each HTML element and parse out the details into a row. """

        time = datetime.datetime.now().strftime("%d/%b/%Y %H:%M")
        meta: MetaJson = {}     # type: ignore

        works = page.find_all(class_="work blurb group")
        for work in works:
            meta.update(self._get_header(work))
            meta.update(self._get_required_tags(work))
            meta.update(self._get_tags(work))
            meta.update(self._get_stats(work))
            meta['fandom'] = self._get_fandoms(work)
            meta['summary'] = self._get_summary(work)
            meta['series_part'], meta['series_name'] = self._get_series(work)
            meta['updated'] = self._get_updated(work)
            meta['scrape_date'] = time

            yield meta

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
                self.logger.info('Attempting to scrape 1 page.')
                return 1
            except ConnectTimeout:
                self.logger.error(f'Base URL: {self.base_url} Not found. '
                                  f'{cfg.MAX_ERRORS-attempts} attempts left.')
        raise ConnectTimeout
        return 0

    def _get_tags(self, meta: BeautifulSoup) -> Any:
        """Find relationships, characters, and freeforms tags"""
        tag_dict = {}   # type: Dict[str, Optional[List[str]]]
        tags = ['relationships', 'characters', 'freeforms']
        for tag in tags:
            tag_dict[tag] = self._get_tag_info(tag, meta)
        return tag_dict

    def _get_tag_info(self, category: str, meta: BeautifulSoup) -> \
            Optional[List[str]]:
        """ Find relationships, characters, and freeforms tags."""
        try:
            tag_list = meta.find_all("li", class_=category)
        except AttributeError:
            return None
        return [result.text for result in tag_list]

    def _get_required_tags(self, work: BeautifulSoup) -> Any:
        """Finds required tags."""
        req_dict = {}
        try:
            req_tags = work.find(class_='required-tags').find_all('a')
            req_dict['rating'] = req_tags[0].text
            req_dict['warnings'] = req_tags[1].text.split(',')
            req_dict['category'] = req_tags[2].text.split(',')
            req_dict['status'] = req_tags[3].text
        except Exception:
            req_dict['rating'] = None
            req_dict['warnings'] = []
            req_dict['category'] = []
            req_dict['status'] = None
        return req_dict

    def _get_stats(self, work: BeautifulSoup) -> Any:
        """
        Find stats (language, published, status, date status, words, chapters,
        comments, kudos, bookmarks, hits
        """
        str_categories = ['language', 'chapters']
        num_categories = ['collections', 'words', 'comments', 'kudos',
                          'bookmarks', 'hits']
        stats = {}
        for s_cat in str_categories:
            try:
                stats[s_cat] = work.find("dd", class_=s_cat).text
            except AttributeError:
                stats[s_cat] = None
        for n_cat in num_categories:
            try:
                str_num = work.find("dd", class_=n_cat).text
                stats[n_cat] = int(str_num.replace(',', ''))
            except (AttributeError, ValueError):
                stats[n_cat] = 0
        return stats

    def _get_header(self, work: BeautifulSoup) -> Any:
        '''Finds header information
           (work_id, title, author, gifted to user).'''
        header_dict = {}

        result = work.find('h4', class_='heading').find_all('a')
        header_dict['work_id'] = result[0].get('href').strip('/works/')
        header_dict['title'] = result[0].text

        auth_list = []
        header_text = work.find('h4', class_='heading').text
        if "Anonymous" in header_text:
            header_dict['author'] = ["Anonymous"]
        else:
            authors = work.find_all('a', rel='author')
            for author in authors:
                auth_list.append(author.text)
            header_dict['author'] = auth_list

        gift_list = []
        for link in result:
            href = link.get('href')
            if 'gifts' in href:
                gift_list.append(link.text)

        if len(gift_list) == 0:
            header_dict['gifted'] = []
        else:
            header_dict['gifted'] = gift_list

        return header_dict

    def _get_fandoms(self, work: BeautifulSoup) -> List[str]:
        """ Find the list of fandoms."""
        try:
            tag_list = work.find('h5', class_='fandoms heading').find_all('a')
            fan_list = [x.text for x in tag_list]
            return fan_list
        except AttributeError:
            return []

    def _get_summary(self, work: BeautifulSoup) -> Optional[str]:
        """ Find summary description and return as list of strings. """

        try:
            summary_string = work.find('blockquote',
                                       class_='userstuff summary')
            summary = summary_string.text.strip().replace('\n', ' ')
        except AttributeError:
            summary = None
        return summary

    def _get_updated(self, work: BeautifulSoup) -> Optional[str]:
        """ Find update date. Return as list of strings. """

        try:
            date = work.find('p', class_='datetime').text
        except AttributeError:
            date = None
        return date

    def _get_series(self, work: BeautifulSoup) \
            -> Tuple[Optional[str], Optional[str]]:
        """ Find series info and return as list. """

        try:
            series = work.find('ul', class_='series')
            part = series.find('strong').text
            s_name = series.find('a').text
        except AttributeError:
            part, s_name = None, None
        return part, s_name

    def _start_from_top(self, from_top: bool) -> bool:

        if from_top is True:
            self.logger.info("Scraping from the top.")
            return True
        elif self.last == self.progress.unscraped_flag:
            self.logger.info(
                f"Last scraped unknown: {self.progress.unscraped_flag}. "
                f"Scraping from the top.")
            return True
        else:
            self.logger.info(f"Picking up from {self.last} ")
            return False
