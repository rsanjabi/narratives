''' In progress refactoring of meta scraping functionality.'''
import time
import datetime
import json
from typing import Generator, Tuple, List
from mypy_extensions import TypedDict

from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout, HTTPError

from scrape.page import Page
import utils.paths as paths
import config as cfg

KudosJson = TypedDict('KudosJson', {
                     'work_id': str,
                     'kudos': List[str],
                     'scrape_date': str})


class Kudos(Page):

    def __init__(self, fandom: str, from_top: bool = True):
        self.log_path = paths.kudo_log_path(fandom)
        self.kudo_path = paths.kudo_path(fandom)
        self.input_path = paths.meta_path(fandom)
        url = (f'https://archiveofourown.org/works/')
        super().__init__(fandom, 'kudos',
                         self.log_path,
                         self.kudo_path,
                         url,
                         from_top)

    def scrape(self):
        super().scrape()

    def _pages(self) -> Generator[Tuple[BeautifulSoup, str], None, None]:

        if self.from_top is True or self.last == self.progress.unscraped_flag:
            encountered = True
        else:
            encountered = False

        errors = 0

        with open(self.input_path, 'r') as f_in:
            for row_str in f_in:
                row = json.loads(row_str)
                if not encountered:
                    if row['work_id'] == self.last:
                        encountered = True
                    continue
                url = self.base_url + row['work_id'] + '/kudos'
                self.fandom_id = row['work_id']
                try:
                    soup = self._get_soup(url)
                    self.logger.info(f"Scraped id: {self.fandom_id}")
                except HTTPError:
                    self.logger.info(f"HTTPError/skipping: {self.fandom_id}")
                except ConnectTimeout:
                    self.logger.error(f"ConnectionTimeout "
                                      f"on: {self.fandom_id}")
                    if errors > cfg.MAX_ERRORS:
                        self.logger.error(f"{cfg.MAX_ERRORS} "
                                          f"encountered. Aborting.")
                        return
                    self.logger.error(f"{cfg.MAX_ERRORS-errors} errors left.")
                    errors += 1
                    time.sleep(cfg.DELAY*errors*10)    # Increase sleep time
                else:
                    yield soup, self.fandom_id
                finally:
                    time.sleep(cfg.DELAY)

    def _page_elements(self, soup: BeautifulSoup) -> Generator[KudosJson,
                                                               None, None]:
        k_d: KudosJson = {}       # type: ignore
        k_d['work_id'] = self.fandom_id
        k_d['kudos'] = [x.text for x in soup.find(id="kudos").find_all('a')]
        k_d['scrape_date'] = datetime.datetime.now().strftime("%d/%b/%Y %H:%M")
        yield k_d
