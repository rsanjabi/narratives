''' In progress refactoring of meta scraping functionality.'''
import time
# import datetime
from typing import Generator, List, Tuple, Any
from urllib.parse import quote

from scrape.page import Page
import utils.paths as paths
import config as cfg


class Meta(Page):

    def __init__(self, fandom: str, from_top: bool):
        self.log_path = paths.meta_log_path(fandom)
        self.meta_path = paths.meta_path(fandom)
        url = (f'https://archiveofourown.org/tags/'
               f'{quote(fandom)}/works?page=')
        super().__init__(fandom, 'meta',
                         self.log_path,
                         self.meta_path,
                         url,
                         from_top)

    def insert(self):
        pass

    def scrape(self):
        header = ['work_id', 'title', 'author', 'gifted', 'rating',
                  'warnings', 'category', 'status', 'fandom',
                  'relationship', 'character', 'additional tags',
                  'summary', 'language', 'words', 'chapters',
                  'collections', 'comments', 'kudos', 'bookmarks',
                  'hits', 'series_part', 'series_name', 'updated',
                  'scrape_date']
        super().scrape(header)

    def _get_pages(self) -> Generator[Tuple[str, str], None, None]:

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
        except Exception as e:
            self.logger.error(f'Base URL: {self.base_url} Not found after '
                              f'{cfg.MAX_ERRORS} (MAX) attempts.')
            raise Exception(e)

        while errors < cfg.MAX_ERRORS and page_num <= max_pages:
            try:
                url = self.base_url + str(page_num)
                soup = self._get_soup(url)
            except Exception:
                errors += 1
                self.logger.error(f'PAGE: {url} Not found. '
                                  f'{cfg.MAX_ERRORS-errors} attempts left.')
                time.sleep(cfg.DELAY*errors)   # exponential decay wait
            else:
                self.logger.info(f'Scraping PAGE: {str(page_num)}')
                time.sleep(cfg.DELAY)
                yield (soup.get_text, str(page_num))
                page_num += 1
                url = self.base_url + str(page_num)

    def _total_pages(self):
        ''' Make max attempts at loading base url to get starting number'''

        for attempts in range(cfg.MAX_ERRORS):
            try:
                soup = self._get_soup(self.base_url)
                next_element = soup.find('li', class_='next')
                max_pages = int(next_element.find_previous('li').text)
                self.logger.info(f'Attempting to scrape up to '
                                 f'{str(max_pages)} pages.')
                return max_pages
            except Exception:
                self.logger.error(f'Base URL: {self.base_url} Not found. '
                                  f'{cfg.MAX_ERRORS-attempts} attempts left.')
            return Exception

    def _get_data(self, soup: str) -> List[Any]:
        print(f"DEBUG1")
        return ['a']

    def _write_results(self):
        print(f"DEBUG2")
        pass
